import os
import uuid
from typing import Optional, List, Tuple, Dict

import aiofiles

from src.utils.schemas import BodyMessage, BodyParticipant, BodyTransaction, HeadMessage
from config import NOT_SEND

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

    @staticmethod
    async def write_to_file(value) -> Optional:
        new_not_send_file = os.path.join(NOT_SEND, f'{uuid.uuid4()}.json')
        async with aiofiles.open(new_not_send_file, 'w') as file:
            # Write all the verified data to a json file, and do not praise the work
            await file.write(str(value))

    @staticmethod
    async def message_packaging(message: List[Dict]) -> Tuple[HeadMessage, BodyMessage]:
        pass