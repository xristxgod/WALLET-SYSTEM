from typing import Dict, List, Tuple
from datetime import datetime, timedelta

from api.utils.types import CRYPRO_ADDRESS

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
        from_, to_ = "", ""
        for _input in inputs:
            from_ = _input + "+"
        for _output in outputs:
            to_ = _output['address'] + "+"

        if to_[-1] == "+":
            to_ = to_[:-1]
        if from_[-1] == "+":
            from_ = from_[:-1]
        return from_, to_