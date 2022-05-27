import decimal
import json
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta

from api.utils.types import CRYPRO_ADDRESS, default_json
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
    def get_inputs(inputs: List[CRYPRO_ADDRESS], amount: decimal.Decimal) -> List[Dict[CRYPRO_ADDRESS, str]]:
        return_data = []
        if len(inputs) == 1:
            return_data.append({"address": inputs[0], "amount": amount})
        else:
            _amount = amount
            amount_for_one = amount / len(inputs)
            for address in inputs:
                if _amount - amount_for_one < 0:
                    return_data.append({
                        "address": address,
                        "amount": _amount
                    })
                else:
                    _amount -= amount_for_one
                    return_data.append({
                        "address": address,
                        "amount": amount_for_one
                    })
        return return_data

    @staticmethod
    def get_amount(outputs: List[Dict]) -> decimal.Decimal:
        amount = decimals.create_decimal(0)
        for _output in outputs:
            amount += decimals.create_decimal(_output.get('amount'))
        return amount

    @staticmethod
    def get_timestamp_now() -> int:
        return int(datetime.timestamp(datetime.now()))

    @staticmethod
    def get_correct_inputs(inputs: List[CRYPRO_ADDRESS], amount: decimal.Decimal) -> json:
        returned_data = []
        if len(inputs) == 1:
            returned_data.append({"address": inputs[0], "amount": amount})
        else:
            summa = amount // len(inputs)
            _amount = amount
            for address in inputs:
                if _amount - summa >= 0:
                    returned_data.append({
                        "address": address,
                        "amount": summa
                    })
                else:
                    returned_data.append({
                        "address": address,
                        "amount": _amount
                    })
        return json.loads(json.dumps(returned_data, default=default_json))
