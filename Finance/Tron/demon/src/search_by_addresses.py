import asyncio
import random
import requests
from typing import List, Dict

from src.__init__ import DB
from src.types import TAddress
from src.utils import Utils
from src.demon import TransactionDemon
from config import Config, logger

class AddressesDemon(TransactionDemon):

    @staticmethod
    def get_all_blocks_by_list_addresses(list_addresses: List[TAddress]) -> List[int]:
        blocks = []
        for address in list_addresses:
            blocks.extend(AddressesDemon.get_all_transactions_block_by_address(address=address))
        return sorted(blocks)

    @staticmethod
    def get_all_transactions_block_by_address(address: TAddress) -> List[int]:
        headers = {"Accept": "application/json", "TRON-PRO-API-KEY": Utils.get_tron_gird_key()}
        url = f"https://api.{'' if AddressesDemon.NETWORK == 'mainnet' else f'{AddressesDemon.NETWORK.lower()}.'}trongrid.io/v1/accounts/{address}/transactions?limit=200"
        response = requests.get(url, headers=headers).json()
        if "data" in response and len(response["data"]) == 0:
            return []
        return sorted([block["blockNumber"] for block in response["data"]])

    @staticmethod
    def fix_list(list_block: List[int], start_block: int = None, end_block: int = None) -> List[int]:
        blocks = []
        for block in list_block:
            if start_block >= block <= end_block:
                blocks.append(block)
        return blocks

    async def start(
            self, start_block: int = None, end_block: int = None,
            list_addresses: List[TAddress] = None,  list_blocks: List[int] = None
    ):
        if list_addresses is None or list_addresses == "all":
            addresses: List = await DB.get_addresses()
        else:
            addresses: List = list_addresses
        logger.error(f"LIST OF ADDRESSES: {addresses}")
        list_block = AddressesDemon.get_all_blocks_by_list_addresses(list_addresses=list_addresses)
        logger.error("SEARCH BLOCKS")
        if not start_block and not end_block and list_blocks is None:
            await self.start_in_list_block(list_blocks=list_block, list_addresses=addresses)
        elif not start_block and not end_block and list_blocks is not None:
            await self.start_in_list_block(list_blocks=list_blocks, list_addresses=addresses)
        elif not start_block and end_block:
            await self.start_in_list_block(
                list_blocks=AddressesDemon.fix_list(list_block=list_block, start_block=1, end_block=end_block),
                list_addresses=addresses
            )
        elif start_block and not end_block:
            await self.start_in_list_block(
                list_blocks=AddressesDemon.fix_list(
                    list_block=list_block,
                    start_block=1,
                    end_block=(await self.get_node_block_number())
                ),
                list_addresses=addresses
            )
        else:
            await self.start_in_range(start_block=start_block, end_block=end_block, list_addresses=addresses)