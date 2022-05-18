import decimal
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

from api.utils.types import CRYPRO_ADDRESS
from config import decimals

class Utils:
    @staticmethod
    def is_have_time(timestamp: int, minutes: int = 15, seconds: int = 30) -> bool:
        timestamp = datetime.fromtimestamp(timestamp)
        timestamp_plus_min = timestamp + timedelta(minutes=minutes, seconds=seconds)
        if datetime.timestamp(timestamp) <= datetime.timestamp(timestamp_plus_min) > datetime.timestamp(datetime.now()):
            return True
        else:
            return False

    @staticmethod
    def get_inputs_and_outputs(inputs: List[CRYPRO_ADDRESS], outputs: List[Dict[CRYPRO_ADDRESS, str]]) -> Tuple:
        from_address, to_address = "", ""
        for _input in inputs:
            from_address = _input + "+"
        for _output in outputs:
            to_address = _output['address'] + "+"
        return from_address[:-1], to_address[:-1]

    @staticmethod
    def get_inputs_and_outputs_for_text(inputs: List[CRYPRO_ADDRESS], outputs: List[Dict[CRYPRO_ADDRESS, str]]) -> Tuple:
        from_address, to_address = "", ""
        for _input in inputs:
            from_address += f"{_input} | "
        for _output in outputs:
            to_address += f"{_output.get('address')} | "
        return from_address[:-3], to_address[:-3]

    @staticmethod
    def get_amount(outputs: List[Dict[CRYPRO_ADDRESS, str]]) -> decimal.Decimal:
        amount = decimals.create_decimal(0)
        for _output in outputs:
            amount += decimals.create_decimal(_output.get('address'))
        return amount