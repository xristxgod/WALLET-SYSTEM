import os
import uuid
from typing import Optional, List, Tuple, Dict

import aiofiles

from src.utils.schemas import BodyMessage, BodyParticipant, BodyTransaction, HeadMessage
from config import NOT_SEND

class Utils:

    @staticmethod
    def is_address(address: str, data: List[BodyParticipant]) -> bool:
        for d in data:
            if d.address == address:
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
        head: Optional[HeadMessage] = None
        body: Optional[BodyMessage] = None
        for msg in message:
            if msg.get("network") is not None:
                head = HeadMessage(
                    network=msg.get("network"),
                    block=int(msg.get("block"))
                )
            else:
                body = BodyMessage(
                    address=msg.get("address"),
                    transactions=await Utils.__get_transactions(msg.get("transactions"))
                )
        return head, body

    @staticmethod
    async def __get_transactions(transactions: List[Dict]) -> List[BodyTransaction]:
        transactions_list: List[BodyTransaction] = []
        for transaction in transactions:
            transactions_list.append(BodyTransaction(
                time=transaction.get("time"),
                transactionHash=transaction.get("transactionHash"),
                fee=float(transaction.get("fee")),
                amount=float(transaction.get("amount")),
                inputs=await Utils.__get_participants(transaction.get("inputs")),
                outputs=await Utils.__get_participants(transaction.get("outputs")),
                token=transaction.get("token"),
            ))
        return transactions_list

    @staticmethod
    async def __get_participants(participants: List[Dict]) -> List[BodyParticipant]:
        participants_list: List[BodyParticipant] = []
        for participant in participants:
            participants_list.append(BodyParticipant(
                address=participant.get("address"),
                amount=float(participant.get("amount")),
            ))
        return participants_list