import os
import uuid
import decimal
from typing import Optional, List, Dict, Tuple

import aiofiles

from config import NOT_SEND, decimals

class Utils:

    @staticmethod
    async def write_to_file(value) -> Optional:
        new_not_send_file = os.path.join(NOT_SEND, f'{uuid.uuid4()}.json')
        async with aiofiles.open(new_not_send_file, 'w') as file:
            # Write all the verified data to a json file, and do not praise the work
            await file.write(str(value))

    @staticmethod
    def is_have_amount(outputs: List[Dict], balance: decimal.Decimal) -> bool:
        amount: decimal.Decimal = decimals.create_decimal(0.0)
        for output in outputs:
            amount += decimals.create_decimal(output.get("amount"))
        return False if balance < amount else True

    @staticmethod
    def is_have_fee(fee: decimal.Decimal, last_fee: decimal.Decimal, balance_native: decimal.Decimal) -> bool:
        if fee > last_fee and fee - last_fee > 10:
            return False
        if balance_native < fee or balance_native - fee < 10:
            return False
        return True

    @staticmethod
    def get_amount(outputs: List[Dict]) -> str:
        amount: decimal.Decimal = decimals.create_decimal(0.0)
        for output in outputs:
            amount += decimals.create_decimal(output.get("amount"))
        return "%.8f" % amount

    @staticmethod
    def error_message(user: str, fee: Dict[str, decimal.Decimal], data: Tuple, title: str = None) -> str:
        if title is None:
            title = "When creating a transaction, something went wrong!\n"
        return (
            f"{title}"
            f"From: {user}\n"
            f"To: {data[0]}\n"
            f"For the amount of: {data[1]} {data[2]}\n"
            f"Fee: {fee.values()} {fee.keys()}"
        )
