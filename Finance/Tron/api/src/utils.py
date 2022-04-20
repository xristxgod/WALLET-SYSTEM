import json
import datetime

from decimal import Decimal, localcontext
from typing import Union, Dict

from src.types import TAddress

class TronUtils:

    SUN = Decimal("1000000")
    MIN_SUN = 0
    MAX_SUN = 2 ** 256 - 1

    @staticmethod
    def from_sun(num: Union[int, float]) -> Union[int, Decimal]:
        """
        Helper function that will convert a value in TRX to SUN
        :param num: Value in TRX to convert to SUN
        """
        if num == 0:
            return 0
        if num < TronUtils.MIN_SUN or num > TronUtils.MAX_SUN:
            raise ValueError("Value must be between 1 and 2**256 - 1")

        unit_value = TronUtils.SUN

        with localcontext() as ctx:
            ctx.prec = 999
            d_num = Decimal(value=num, context=ctx)
            result = d_num / unit_value

        return result

    @staticmethod
    def to_sun(num: Union[int, float]) -> int:
        """
        Helper function that will convert a value in TRX to SUN
        :param num: Value in TRX to convert to SUN
        """
        if isinstance(num, int) or isinstance(num, str):
            d_num = Decimal(value=num)
        elif isinstance(num, float):
            d_num = Decimal(value=str(num))
        elif isinstance(num, Decimal):
            d_num = num
        else:
            raise TypeError("Unsupported type. Must be one of integer, float, or string")

        s_num = str(num)
        unit_value = TronUtils.SUN

        if d_num == 0:
            return 0

        if d_num < 1 and "." in s_num:
            with localcontext() as ctx:
                multiplier = len(s_num) - s_num.index(".") - 1
                ctx.prec = multiplier
                d_num = Decimal(value=num, context=ctx) * 10 ** multiplier
            unit_value /= 10 ** multiplier

        with localcontext() as ctx:
            ctx.prec = 999
            result = Decimal(value=d_num, context=ctx) * unit_value

        if result < TronUtils.MIN_SUN or result > TronUtils.MAX_SUN:
            raise ValueError("Resulting wei value must be between 1 and 2**256 - 1")

        return int(result)

class TransactionUtils:

    @staticmethod
    def get_transaction_body(
            txn: Dict, fee: str, from_address: TAddress, to_address: TAddress, amount: str, token: str = None
    ):
        return json.dumps({
            "time": int(datetime.datetime.timestamp(datetime.datetime.now())),
            "transactionHash": txn["txID"],
            "transactionType": txn["raw_data"]["contract"][0]["type"],
            "fee": fee,
            "amount": amount,
            "senders": [
                {
                    "address": from_address,
                    "amount": amount,
                },
            ],
            "recipients": [
                {
                    "address": to_address,
                    "amount": amount,
                },
            ],
            "token": token if token is not None else "-"
        })