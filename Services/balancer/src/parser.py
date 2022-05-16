from typing import Optional, Dict, List

from src.utils import Utils
from src.services.crypto import CryptForUser
from config import decimals, logger

class Parser:

    @staticmethod
    async def is_enough(user: CryptForUser, outputs: List[Dict]) -> Optional[str]:
        for _, balance in (await user.get_balances()).items():
            if not Utils.is_have_amount(outputs=outputs, balance=balance):
                to, amount, network = user.get_outputs(outputs=outputs)
                return (
                    "There is not enough balance to send the transaction!\n"
                    f"From: {user}\n"
                    f"To: {to}\n"
                    f"For the amount of: {amount} {network}\n"
                    f"Fee: {user.BASE_FEE} {user.native}"
                )
        for _, balance_native in (await user.get_balances(token=user.native)).items():
            if not Utils.is_have_fee(
                    fee=(await user.get_optimal_fee(outputs=outputs)),
                    last_fee=user.BASE_FEE,
                    balance_native=balance_native
            ):
                to, amount, network = user.get_outputs(outputs=outputs)
                return (
                    f"There is not enough {user.native.upper()} on your wallet to pay the commission!\n"
                    f"From: {user}\n"
                    f"To: {to}\n"
                    f"For the amount of: {amount} {network}\n"
                    f"Fee: {user.BASE_FEE} {user.native}"
                )

    @staticmethod
    async def start_sending(user: CryptForUser, outputs: List[Dict]) -> Optional:
        is_enough: Optional[str] = await Parser.is_enough(user=user, outputs=outputs)
        if is_enough is not None:
            return is_enough
        create_tx = await user.create_transaction(outputs=outputs)
        if create_tx is None:
            return (
                ""
            )

    @staticmethod
    async def processing_message(data: Dict):
        try:
            user = CryptForUser(
                network=data["network"],
                token=data["token"],
                inputs=["inputs"]
            )
            user.CHAT_ID = data.get("chatID")
            user.BASE_FEE = decimals.create_decimal(data.get("fee"))
            status = await Parser.start_sending(user=user, outputs=data.get("outputs"))
            if status is not None:
                pass
        except Exception as error:
            logger.error("ERROR: error")
            pass