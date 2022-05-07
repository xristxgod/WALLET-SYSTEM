from typing import Union, Optional, List, Tuple, Dict

class Utils:

    @staticmethod
    def is_address(address: str, data: List[Dict]) -> bool:
        for d in data:
            if d.get("address") == address:
                return True
        else:
            return False
