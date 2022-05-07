from typing import Union, Optional, List, Tuple, Dict

class Utils:

    @staticmethod
    def is_address(address: str, data: List[Dict]) -> bool:
        for d in data:
            if d.get("address") == address:
                return True
        else:
            return False

    @staticmethod
    def get_addresses_for_send(addresses_data: List) -> str:
        text = ""
        for address in addresses_data:
            text += f"{address} | "
        return text[0:-3]