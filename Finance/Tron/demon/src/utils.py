import os
import json
import base58
import uuid
import decimal
from typing import Union, Dict
from datetime import datetime

import aiofiles

from config import NOT_SEND, ERROR, LAST_BLOCK, decimals

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

class TronUtils:

    SUN = decimal.Decimal("1000000")
    MIN_SUN = 0
    MAX_SUN = 2 ** 256 - 1

    @staticmethod
    def to_base58check_address(raw_addr: Union[str, bytes]) -> str:
        """Convert hex address or base58check address to base58check address(and verify it)."""
        if isinstance(raw_addr, (str,)):
            if raw_addr[0] == "T" and len(raw_addr) == 34:
                try:
                    # assert checked
                    base58.b58decode_check(raw_addr)
                except ValueError:
                    raise Exception("bad base58check format")
                return raw_addr
            elif len(raw_addr) == 42:
                if raw_addr.startswith("0x"):  # eth address format
                    return base58.b58encode_check(b"\x41" + bytes.fromhex(raw_addr[2:])).decode()
                else:
                    return base58.b58encode_check(bytes.fromhex(raw_addr)).decode()
            elif raw_addr.startswith("0x") and len(raw_addr) == 44:
                return base58.b58encode_check(bytes.fromhex(raw_addr[2:])).decode()
        elif isinstance(raw_addr, (bytes, bytearray)):
            if len(raw_addr) == 21 and int(raw_addr[0]) == 0x41:
                return base58.b58encode_check(raw_addr).decode()
            if len(raw_addr) == 20:  # eth address format
                return base58.b58encode_check(b"\x41" + raw_addr).decode()
            return TronUtils.to_base58check_address(raw_addr.decode())
        raise Exception(repr(raw_addr))

    @staticmethod
    def from_sun(num: Union[int, float]) -> Union[int, decimal.Decimal]:
        """
        Helper function that will convert a value in TRX to SUN
        :param num: Value in TRX to convert to SUN
        """
        if num == 0:
            return 0
        if num < TronUtils.MIN_SUN or num > TronUtils.MAX_SUN:
            raise ValueError("Value must be between 1 and 2**256 - 1")

        unit_value = TronUtils.SUN

        with decimal.localcontext() as ctx:
            ctx.prec = 999
            d_num = decimal.Decimal(value=num, context=ctx)
            result = d_num / unit_value

        return result

class DemonUtils:
    @staticmethod
    async def get_last_block_number() -> Union[int, None]:
        """Get the block number recorded in the "last_block.txt" file"""
        async with aiofiles.open(LAST_BLOCK, "r") as file:
            last_block = await file.read()
        if last_block:
            return int(last_block)

    @staticmethod
    async def save_block_number(block_number: int):
        """
        Save the current block to a file "last_block.txt"
        :param block_number: The number of the block to be recorded
        """
        async with aiofiles.open(LAST_BLOCK, "w") as file:
            await file.write(str(block_number))

    @staticmethod
    async def smart_contract_transaction(data: str, token_info: Dict) -> Dict:
        """
        Unpacking a smart contract
        :param data: Smart Contract Information
        :param token_info: Smart contract (Token TRC20) info
        """
        return {
            "to_address": TronUtils.to_base58check_address("41" + data[32:72]),
            "token": token_info["token"],
            "amount": "%.8f" % decimals.create_decimal(int("0x" + data[72:], 0) / 10 ** int(token_info["decimals"]))
        }

class Utils:

    @staticmethod
    def get_helper_file_name() -> str:
        return os.path.join(NOT_SEND, f'{int(datetime.timestamp(datetime.now()))}-{uuid.uuid4()}.json')

    @staticmethod
    def convert_time(timestamp: int) -> str:
        """
        Convert from timestamp to date and time
        :param timestamp: Timestamp data
        """
        return datetime.fromtimestamp(int(timestamp)).strftime('%d-%m-%Y %H:%M:%S')