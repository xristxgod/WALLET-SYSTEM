import json
from typing import Optional, List, Dict

import aiofiles

from config import ENDPOINTS_FILE

class Endpoint:

    ENDPOINTS = {
        "FINANCE": ["TRON"],
        "SERVICES": ["SENDER", "COINCER"],
        "ADMIN": ["SITE"],
        "BOT": ["BOT_MAIN", "BOT_ALERT"]
    }

    @staticmethod
    def __is_mod_in_sub(sub_name: str, mod_name: str) -> bool:
        for endpoint_name, endpoint_value in Endpoint.ENDPOINTS.items():
            if endpoint_name == sub_name.upper() and mod_name.upper() in endpoint_value:
                return True
        else:
            return False

    @staticmethod
    def __is_sub(sub_name: str) -> bool:
        for endpoint_name, endpoint_value in Endpoint.ENDPOINTS.items():
            if endpoint_name == sub_name.upper():
                return True
        else:
            return False

    @staticmethod
    async def __get_endpoints_file() -> Dict:
        async with aiofiles.open(ENDPOINTS_FILE, "a", encoding='utf-8') as file:
            return json.loads(await file.read())

    @staticmethod
    async def get_all_endpoints() -> List[Dict]:
        """Get all the endpoints for verification"""
        endpoints: Optional[List[Dict]] = []
        for endpoint_key, endpoint_value in (await Endpoint.__get_endpoints_file()).items():
            for _, end_value in endpoint_value:
                endpoints.append(*end_value)
        return endpoints

    @staticmethod
    async def get_endpoints(sub_name: str = None, mod_name: str = None) -> List[Dict]:
        """
        Get a separate module with endpoint or a subsystem.
        :param sub_name: The name of the subsystem.
        :param mod_name: The name of the module.
        """
        if sub_name is None and mod_name is None:
            return await Endpoint.get_all_endpoints()
        elif sub_name is None and mod_name is not None:
            raise Exception("We can`t return modules without knowing the subsystem!")
        else:
            if sub_name is not None and mod_name is None and not Endpoint.__is_sub(sub_name=sub_name):
                raise Exception(f"We could not find this subsystem '{sub_name}'!")
            elif sub_name is not None and mod_name is not None and not Endpoint.__is_mod_in_sub(sub_name, mod_name):
                raise Exception(f"We could not find this module '{mod_name}' in this subsystem {sub_name}!")

        endpoints: Optional[List[Dict]] = []
        for endpoint_key, endpoint_value in (await Endpoint.__get_endpoints_file()).items():
            if endpoint_key == sub_name:
                for end_name, end_value in endpoint_value:
                    if end_name == mod_name:
                        endpoints.append(*end_value)
        return endpoints