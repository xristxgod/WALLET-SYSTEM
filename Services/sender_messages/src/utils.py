import os
import uuid
import json
from typing import Union, Dict
from datetime import datetime

import aiofiles

from src.types import emojis
from config import ERROR, NOT_SEND

class Errors:

    @staticmethod
    async def write_to_error(error: Exception, msg: str):
        async with aiofiles.open(ERROR, 'a', encoding='utf-8') as file:
            # If an error occurred on the RabbitMQ side, write about it.
            await file.write(f"Error: {error} | {msg} \n")

    @staticmethod
    async def write_to_helper_file(values: json):
        async with aiofiles.open(Utils.get_helper_file_name(), 'w') as file:
            # Write all the verified data to a json file, and do not praise the work
            await file.write(values)

    @staticmethod
    async def write_to_send(error: Exception, msg: str, title: str, func: str) -> json:
        return json.dumps({
            "status": "ERROR",
            "time": Utils.get_datetime(),
            "title": title,
            "func": func,
            "error": f"{error}",
            "message": msg,
        })

class ParserDemonUtils:

    COINS = {
        "TRON": {"fee": "TRX"}
    }

    @staticmethod
    def get_coin(network: str, token: str = None) -> Dict:
        for network_name, values in ParserDemonUtils.COINS:
            if network_name == network.upper():
                return {
                    "fee": values["fee"],
                    "amount": values["fee"] if token is None else token
                }

class BotUtils:

    @staticmethod
    def generate_report_add(tx_info: Dict, status: str, network: str, coin: str, fee_coin: str):
        if status == "add":
            title = (
                f"{emojis.GREEN_CIRCLE} There was a replenishment:\n"
                f"Sender: {tx_info['senders'][0]['address']}\n"
            )
        else:
            title = (
                f"{emojis.RED_CIRCLE} Debiting has occurred:\n"
                f"Recipient: {tx_info['recipients'][0]['address']}"
            )
        return (
            f"{title}"
            f"For the amount of: {tx_info['amount']} {coin}\n"
            f"Fee: {tx_info['fee']} {fee_coin}\n"
            f"Network: {network} {emojis.get_network_emoji(network=network, coin=coin)}\n"
            f"On the blockchain:\n"
            f"{emojis.get_blockchain_url(network=network, tx_hash=tx_info['transactionHash'])}"
        )

class Utils:

    @staticmethod
    def get_helper_file_name() -> str:
        return os.path.join(NOT_SEND, f'{int(datetime.timestamp(datetime.now()))}-{uuid.uuid4()}.json')

    @staticmethod
    def get_datetime(is_timestamp: bool = True) -> Union[int, str]:
        date = datetime.now()
        if is_timestamp:
            return int(datetime.timestamp(date))
        return date.strftime('%Y-%m-%d %H:%M:%S')
