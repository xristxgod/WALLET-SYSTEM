from typing import List, Dict

from src.parser import Parser

async def parser_message_service(data: Dict):
    await Parser.processing_message(data=data)