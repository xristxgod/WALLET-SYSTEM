from typing import Optional, Dict, List, Union

import aio_pika

from src.__init__ import DB, RabbitMQ
from src.utils import Utils
from src.sender import SenderToBotAlert
from src.services.crypto import CryptForUser
from config import decimals, logger

class Parser:

    @staticmethod
    async def is_enough(user: CryptForUser, outputs: List[Dict]) -> Optional[str]:
        for _, balance in (await user.get_balances()).items():
            if not Utils.is_have_amount(outputs=outputs, balance=balance):
                logger.error(
                    f"The user: {user.CHAT_ID} does not have enough funds on the balance to send the transaction!"
                )
                return Utils.error_message(
                    user=str(user),
                    fee={user.native: user.BASE_FEE},
                    data=user.get_outputs(outputs=outputs),
                    title=f"There is not enough balance {user.token.upper()} to send the transaction!\n"
                )
        logger.info(f"The user: {user.CHAT_ID} has enough funds on the balance to send the transaction!")
        for _, balance_native in (await user.get_balances(token=user.native)).items():
            if not Utils.is_have_fee(
                    fee=(await user.get_optimal_fee(outputs=outputs)),
                    last_fee=user.BASE_FEE,
                    balance_native=balance_native
            ):
                logger.error(f"The user: {user.CHAT_ID} does not have enough funds on the balance to pay the commission!")
                return Utils.error_message(
                    user=str(user),
                    fee={user.native: user.BASE_FEE},
                    data=user.get_outputs(outputs=outputs),
                    title=f"There is not enough {user.native.upper()} on your wallet to pay the commission!\n"
                )
        logger.info(f"The user: {user.CHAT_ID} has enough funds on the balance to send the transaction!")

    @staticmethod
    async def create(user: CryptForUser, outputs: List[Dict]) -> Union[Dict[str], str]:
        """Create transaction"""
        create_tx = await user.create_transaction(outputs=outputs)
        if create_tx is None:
            logger.error(f"When creating a transaction for the user: {user.CHAT_ID} something went wrong!")
            return Utils.error_message(
                user=str(user),
                fee={user.native: user.BASE_FEE},
                data=user.get_outputs(outputs=outputs),
            )
        logger.info(f"Transactions for the user: {user.CHAT_ID} has been created!")
        transaction_body: Dict = create_tx.get("bodyTransaction")
        try:
            is_transaction = DB.update_transaction(
                chat_id=user.CHAT_ID,
                network=user.network,
                status=1,
                last_status=0,
                transaction_hash=transaction_body.get("transactionHash"),
                fee=create_tx.get("fee")
            )
        except Exception as error:
            logger.error(f"ERROR: {error}")
            is_transaction = DB.add_new_transaction(
                chat_id=user.CHAT_ID, network=user.network, status=1, token=transaction_body.get("token"),
                time=transaction_body.get("time"), transaction_hash=transaction_body.get("transaction_hash"),
                fee=transaction_body.get("fee"), amount=transaction_body.get("amount"),
                senders=transaction_body.get("senders"), recipients=transaction_body.get("recipients")
            )
        if not is_transaction:
            logger.error(f"Transaction: {transaction_body.get('transactionHash')} was not added to the database!")
            return Utils.error_message(
                user=str(user),
                fee={user.native: user.BASE_FEE},
                data=user.get_outputs(outputs=outputs),
            )
        else:
            logger.info(f"Transaction: {transaction_body.get('transactionHash')} has been added to the database!")
        message_status = await SenderToBotAlert.update_transaction(
            chat_id=user.CHAT_ID,
            status=1,
            network=user.full_network,
            transactionHash=transaction_body.get("transactionHash"),
            fromAddress=user.inputs,
            toAddress=outputs,
            amount=transaction_body.get("amount"),
            fee=transaction_body.get("fee"),
        )
        if not message_status:
            logger.info(f"Transaction: {transaction_body.get('transactionHash')} was not sent to the bot!")
            return Utils.error_message(
                user=str(user),
                fee={user.native: user.BASE_FEE},
                data=user.get_outputs(outputs=outputs),
            )
        else:
            logger.info(f"Transaction: {transaction_body.get('transactionHash')} has been sent to the bot!")
        return {"createTxHex": transaction_body.get("createTxHex"), "txHash": transaction_body.get('transactionHash')}

    @staticmethod
    async def send(user: CryptForUser, create_tx_hax: str, tx_hash: str, outputs: List[Dict]) -> Optional[str]:
        """Send transaction"""
        send_tx = await user.send_transaction(
            create_tx_hex=create_tx_hax,
            private_keys=(await DB.get_private_keys(
                chat_id=user.CHAT_ID,
                network=user.network,
                addresses=tuple(user.inputs)
            ))
        )
        if not send_tx:
            logger.info(f"Transaction: {tx_hash} was not sent!")
            return Utils.error_message(
                user=str(user),
                fee={user.native: user.BASE_FEE},
                data=user.get_outputs(outputs=outputs),
            )
        else:
            logger.info(f"Transaction: {tx_hash} has been sent!")

    @staticmethod
    async def start_sending(user: CryptForUser, outputs: List[Dict]) -> Optional:
        is_enough: Optional[str] = await Parser.is_enough(user=user, outputs=outputs)
        if is_enough is not None:
            return is_enough
        is_create = await Parser.create(user=user, outputs=outputs)
        if isinstance(is_create, str):
            return is_create
        is_send = await Parser.send(
            create_tx_hax=is_create.get("createTxHex"),
            tx_hash=is_create.get("txHash"),
            outputs=outputs
        )
        if is_send is not None:
            return is_send

    @staticmethod
    async def processing_message(data: Dict):
        try:
            user = CryptForUser(
                network=data["network"],
                token=data["token"],
                inputs=data["inputs"]
            )
            user.CHAT_ID = data.get("chatID")
            user.BASE_FEE = decimals.create_decimal(data.get("fee"))
            status = await Parser.start_sending(user=user, outputs=data.get("outputs"))
            if status is not None:
                await SenderToBotAlert.send_info_to_user(chat_id=data.get("chatID"), info=status, to_main=True)
                await SenderToBotAlert.update_transaction(
                    chat_id=data.get("chatID"),
                    status=3,
                    network=user.full_network,
                    transactionHash="-",
                    fromAddress=data["inputs"],
                    toAddress=data['outputs'],
                    amount=user.get_outputs(outputs=data['outputs'])[1],
                    fee=user.BASE_FEE,
                )
        except Exception as error:
            logger.error(f"ERROR: {error}")
            await RabbitMQ.resend_message(message=aio_pika.Message(body=f"{data}".encode()))
            await SenderToBotAlert.update_transaction(
                chat_id=data.get("chatID"),
                status=3,
                network=f"{data.get('network').upper()}_{data.get('token').upper()}",
                transactionHash="-",
                fromAddress=data.get("inputs"),
                toAddress=data.get("outputs"),
                amount=Utils.get_amount(data.get("outputs")),
                fee=data.get("fee")
            )