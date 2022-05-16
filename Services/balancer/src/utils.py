import os
import uuid
import decimal
from typing import Optional, List, Dict

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