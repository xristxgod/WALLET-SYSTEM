from typing import List, Dict

from src.services.parser import Parser

async def parser_message_service(data: List[Dict]):
    await Parser.processing_message(data=data)