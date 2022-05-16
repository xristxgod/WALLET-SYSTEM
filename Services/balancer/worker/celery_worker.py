import asyncio
from typing import List, Dict, Coroutine, Any

from worker.celery_app import celery_app
from worker.services.parser_message import parser_message_service

def run_sync(func: Coroutine[Any]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func)

@celery_app.task(acks_late=True)
def parser_message(data: List[Dict]):
    run_sync(parser_message_service(data=data))