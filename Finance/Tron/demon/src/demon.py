import os
import asyncio
import json
from typing import Optional, List, Dict
from time import time as timer
from datetime import timedelta

import aiofiles
from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

from src.__init__ import DB, RabbitMQ
from src.schemas import BodyTransaction, BodyInputsOrOutputs, BodyMessage
from src.types import TAddress
from src.utils import TronUtils, DemonUtils, Utils, Errors
from config import NOT_SEND, Config, logger, decimals

class TransactionDemon:
    # Provider config
    PROVIDER = AsyncHTTPProvider(Config.TRON_NODE_URL)
    NETWORK: str = "shasta" if Config.NETWORK == "TESTNET" else "mainnet"
    # Tron utils
    fromSun = staticmethod(TronUtils.from_sun)
    toBase58CheckAddress = staticmethod(TronUtils.to_base58check_address)
    # Demon utils
    getLastBlockNumber = staticmethod(DemonUtils.get_last_block_number)
    saveBlockNumber = staticmethod(DemonUtils.save_block_number)
    smartContractTransaction = staticmethod(DemonUtils.smart_contract_transaction)

    def __init__(self):
        """Connect to Tron Node"""
        self.node = AsyncTron(
            provider=self.PROVIDER if self.NETWORK == "mainnet" else None,
            network=self.NETWORK
        )

    async def get_node_block_number(self) -> int:
        """Get the number of the private block in the node"""
        return int(await self.node.get_latest_block_number())

    async def processing_block(self, block_number: int, addresses: List[TAddress]):
        """
        This method receives transactions from the block and processes them
        :param block_number: The number of the block from which to receive transactions
        :param addresses: A list of addresses to search for transactions
        """
        try:
            logger.error(f"{Utils.get_datetime(False)} | PROCESSING BLOCK: {block_number}")
            # Get transactions from the block.
            block = await self.node.get_block(id_or_num=int(block_number))
            if "transactions" in block.keys() and isinstance(block["transactions"], list):
                count_trx = len(block["transactions"])
            else:
                return True
            if count_trx == 0:
                return True
            all_txn_hash_in_db = await DB.get_all_transactions_hash()
            tnx = await asyncio.gather(*[
                self.processing_transaction(
                    tx=block['transactions'][index],
                    addresses=addresses,
                    timestamp=block["block_header"]["raw_data"]["timestamp"],
                    all_txn_hash_in_db=all_txn_hash_in_db
                )
                for index in range(count_trx)
            ])
            tnx = list(filter(lambda x: x is not None, tnx))
            if len(tnx) > 0:
                await asyncio.gather(*[
                    TransactionDemon.send_to_rabbit(
                        package=tx,
                        block_number=block_number
                    ) for tx in tnx
                ])
            return True
        except Exception as error:
            logger.error(f"ERROR DEMON PROCESSING BLOCK STEP 50: {error}")
            await Errors.write_to_error(error=error, msg="ERROR 'TransactionDemon' STEP 50")
            return False

    async def processing_transaction(
            self, tx: Dict, addresses: List[TAddress], timestamp: int, all_txn_hash_in_db: List
    ) -> Optional[BodyMessage]:
        """
        This method analyzes transactions in detail, and searches for the necessary addresses in them.
        :param tx: The transaction that needs to be parsed
        :param addresses: A list of addresses to search for transactions
        :param timestamp: The time of confirmation of the transaction in the block
        :param all_txn_hash_in_db: Hash of transactions that are in the database
        """
        try:
            # If the transaction is not confirmed or with an error, then skip it.
            if tx["ret"][0]["contractRet"] != "SUCCESS":
                return None
            # Value in the transaction
            tx_values = tx["raw_data"]["contract"][0]["parameter"]["value"]
            # Transaction type
            tx_type = tx["raw_data"]["contract"][0]["type"]
            token = None
            # Transaction hash
            tx_hash = tx["txID"]
            # Addresses that are in the transaction.
            tx_addresses = []
            tx_from = None  # Sender
            tx_to = None    # Receiver
            if tx_values["owner_address"] is not None:
                # Recording the sender
                tx_from = TransactionDemon.toBase58CheckAddress(tx_values["owner_address"])
                tx_addresses.append(tx_from)
            if tx_type == "TransferContract" and tx_values["to_address"] is not None:
                # We record the recipient if the transaction was made in the native currency.
                tx_to = TransactionDemon.toBase58CheckAddress(tx_values["to_address"])
                tx_addresses.append(tx_to)
            elif tx_type == "TriggerSmartContract" \
                    and tx_values["contract_address"] in (await DB.get_all_token_address()) \
                    and tx_values["data"] is not None and 140 > len(tx_values["data"]) > 130:
                # We record the recipient if the transaction was made in tokens.
                tx_to = TransactionDemon.toBase58CheckAddress("41" + tx_values["data"][32:72])
                tx_addresses.append(tx_to)

            address = None
            for tx_address in tx_addresses:
                # We are looking for the address of our wallet among the addresses in the transaction.
                if tx_address in addresses:
                    # If we find it, we write it to a variable.
                    address = tx_address
                    break

            if address is not None or tx_hash in all_txn_hash_in_db:
                if address is None:
                    address = tx_from
                if tx_type == "TransferContract":
                    amount = "%.8f" % decimals.create_decimal(TransactionDemon.fromSun(tx_values["amount"]))
                elif tx_type == "TriggerSmartContract":
                    # We analyze data transactions.
                    token = await TransactionDemon.smartContractTransaction(
                        data=tx_values["data"],
                        contract_address=tx_values["contract_address"]
                    )
                    if "data" in token:
                        return None
                    amount = token["amount"]
                else:
                    amount = 0
                # We get a more detailed transaction.
                tx_fee = await self.node.get_transaction_info(tx_hash)
                if "fee" not in tx_fee:
                    fee = 0
                else:
                    fee = decimals.create_decimal(TransactionDemon.fromSun(tx_fee["fee"]))

                values = BodyTransaction(
                    time=timestamp,
                    transactionHash=tx_hash,
                    amount=amount,
                    fee=fee,
                    inputs=[BodyInputsOrOutputs(
                        address=tx_from,
                        amount=amount
                    )],
                    outputs=[BodyInputsOrOutputs(
                        address=tx_to,
                        amount=amount
                    )]
                )

                if token is not None and "data" not in token:
                    # If the transaction was made in a token.
                    values.token = token["token"]
                return BodyMessage(address=address, transactions=[values])
            return None
        except Exception as error:
            logger.error(f"ERROR DEMON PROCESSING TRANSACTION STEP 100: {error}")
            await Errors.write_to_error(error=error, msg="ERROR 'TransactionDemon' STEP 100")
            return None

    @staticmethod
    async def send_to_rabbit(package, block_number) -> None:
        """
        We are preparing transactions to be sent to RabbitMQ
        :param package: Ready transaction
        :param block_number: Block number
        """
        token = (
            package["transactions"][0]["token"].lower()
            if "token" in package['transactions'][0].keys()
            else "trx"
        )
        if token is not None and token != "trx":
            tx_network = f"TRON-{token.upper()}"
        else:
            tx_network = "TRON-TRX"
        # We pack the transaction in a gift box.
        package_for_sending = [
            {
                "network": tx_network,
                "block": block_number
            },
            package
        ]
        try:
            await RabbitMQ.send_to_sender(values=json.dumps(package_for_sending))
        except Exception as error:
            logger.error(f"ERROR DEMON SEND TO RABBIT STEP 212: {error}")
            await Errors.write_to_error(error=error, msg="ERROR 'TransactionDemon' STEP 212")

    async def run(self):
        """The script runs all the time"""
        start = await TransactionDemon.getLastBlockNumber()
        pack_size = 1
        while True:
            end = await self.get_node_block_number()
            if end - start < pack_size:
                await asyncio.sleep(3)
            else:
                start_time = timer()
                addresses = await DB.get_addresses()
                success = await asyncio.gather(*[
                    self.processing_block(block_number=block_number, addresses=addresses)
                    for block_number in range(start, start + pack_size)
                ])
                logger.error("END BLOCK: {}. TIME TAKEN: {} SEC".format(
                    start, str(timedelta(seconds=int(timer() - start_time)))
                ))
                if all(success):
                    start += pack_size
                    await TransactionDemon.saveBlockNumber(block_number=start)
                else:
                    try:
                        raise Exception(f"The block {start} was not recorded")
                    except Exception as error:
                        logger.error(f"ERROR DEMON RUN STEP 232: {error}")
                        await Errors.write_to_error(error=error, msg="ERROR 'TransactionDemon' STEP 232")
                        continue

    async def start_in_range(self, start_block: int, end_block: int, list_addresses: List[TAddress] = None):
        for block_number in range(start_block, end_block):
            if list_addresses is not None:
                addresses = list_addresses
            else:
                addresses = await DB.get_addresses()
            await self.processing_block(block_number=block_number, addresses=addresses)

    async def start_in_list_block(self, list_blocks: List[int], list_addresses: List[TAddress] = None):
        for block_number in list_blocks:
            if list_addresses is not None:
                addresses = list_addresses
            else:
                addresses = await DB.get_addresses()
            await self.processing_block(block_number=int(block_number), addresses=addresses)

    async def start(self, start_block: int = None, end_block: int = None, list_blocks: List[int] = None):
        logger.error((
            "START OF THE SEARCH: "
            f"START BLOCK: {start_block if start_block is not None else 'NOT SPECIFIED'} | "
            f"END BLOCK: {end_block if end_block is not None else 'NOT SPECIFIED'} | "
        ))
        if list_blocks:
            await self.start_in_list_block(list_blocks=list_blocks)
        elif start_block and end_block:
            await self.start_in_range(start_block, end_block)
        elif start_block and not end_block:
            await self.start_in_range(start_block, await self.get_node_block_number() + 1)
        elif not start_block and end_block:
            await self.start_in_range(await self.get_node_block_number(), end_block)
        else:
            await self.send_all_from_folder_not_send()
            await self.run()
        logger.error("END OF SEARCH")

    @staticmethod
    async def send_all_from_folder_not_send(self):
        """Send those transits that were not sent due to any errors"""
        files = os.listdir(NOT_SEND)
        for file_name in files:
            try:
                path = os.path.join(NOT_SEND, file_name)
                async with aiofiles.open(path, 'r') as file:
                    values = await file.read()
                await RabbitMQ.send_to_sender(values=values)
                os.remove(path)
            except Exception as error:
                logger.error(f"ERROR: {error}")
                logger.error(f"NOT SEND: {file_name}")
                continue