
import os
import json
import asyncio
from typing import Optional, List, Dict, Any

import aio_pika
import aiofiles

from src.__init__ import RabbitMQ, observer

from worker.celery_app import celery_app
from config import NOT_SEND, Config, logger

async def processing_message(message: aio_pika.Message) -> Optional:
    """
    Decrypt the message from the queue and send it for forwarding.
    :param message: Message from queue
    """
    try:
        async with message.process():
            msg: List[Dict] = json.loads(message.body)
            logger.error(f"MESSAGE: {msg}")
        can_go, wait_time = await observer.can_go(address=msg[1].get("address"), data=msg)
        extra = {"countdown": wait_time} if not can_go and wait_time > 5 else {}
        celery_app.send_task("worker.celery_worker.parser_message", args=[msg], **extra)
    except Exception as error:
        # Resend method
        logger.error("ERROR: error")
        await RabbitMQ.resend_message(message=message)

async def run(loop: Any) -> Optional:
    """Infinitely included script"""
    while True:
        try:
            connection = None
            while connection is None or connection.is_closed:
                try:
                    # Connect to RabbitMQ
                    connection = await aio_pika.connect_robust(Config.RABBITMQ_URL, loop=loop)
                finally:
                    logger.error(f'WAIT CONNECT TO RABBITMQ')
                await asyncio.sleep(2)
            async with connection:
                # Connect to the RabbitMQ channel
                channel = await connection.channel()
                # Connections to the queue in RabbitMQ by name
                queue = await channel.declare_queue(Config.RABBITMQ_QUEUE_FOR_SENDER, durable=True)
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        await processing_message(message=message)
        except Exception as error:
            logger.error(f"ERROR: {error}")
            await asyncio.sleep(10)
            await send_all_from_folder_not_send()
            continue

# <<<================================>>> Resend script <<<===========================================================>>>

async def send_all_from_folder_not_send() -> Optional:
    """Send those transits that were not sent due to any errors"""
    files = os.listdir(NOT_SEND)
    for file_name in files:
        try:
            path = os.path.join(NOT_SEND, file_name)
            async with aiofiles.open(path, "r") as file:
                values = await file.read()
            await RabbitMQ.resend_message(values=aio_pika.Message(body=f"{values}".encode()))
            os.remove(path)
        except Exception as error:
            logger.error(f"ERROR: {error}")
            continue