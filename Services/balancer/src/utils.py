import os
import uuid
from typing import Optional

import aiofiles

from config import NOT_SEND

class Utils:

    @staticmethod
    async def write_to_file(value) -> Optional:
        new_not_send_file = os.path.join(NOT_SEND, f'{uuid.uuid4()}.json')
        async with aiofiles.open(new_not_send_file, 'w') as file:
            # Write all the verified data to a json file, and do not praise the work
            await file.write(str(value))