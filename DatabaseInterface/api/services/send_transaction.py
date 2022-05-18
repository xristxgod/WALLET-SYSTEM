import decimal
from typing import Optional, List, Dict

from rest_framework.exceptions import ValidationError

from api.models import UserModel, NetworkModel, WalletModel
from api.services.__init__ import BaseApiModel, transaction_repository
from api.services.external.sender import Sender
from api.services.external.queue import Queue
from api.utils.types import CRYPRO_ADDRESS, FULL_NETWORK, NETWORK, TG_CHAT_ID
from api.utils.utils import Utils
from config import Config, decimals, logger

# Body
class BodySendTransactionModel:
    """Type of input data"""
    MIN_AMOUNT = decimals.create_decimal(0)
    MAX_AMOUNT = decimals.create_decimal(1000000000000000)

    def __init__(
            self,
            chatID: TG_CHAT_ID,
            network: FULL_NETWORK,
            outputs: List[Dict[CRYPRO_ADDRESS, str]],
            inputs: Optional[List[CRYPRO_ADDRESS]] = None,
            fee: decimal.Decimal = None,
            is_check: bool = True
    ):
        self.chatID: TG_CHAT_ID = chatID
        self.network: FULL_NETWORK = network.upper()
        self.inputs: List[CRYPRO_ADDRESS] = inputs
        self.outputs: List[Dict[CRYPRO_ADDRESS, str]] = outputs
        self.fee: decimal.Decimal = fee
        if is_check:
            self.is_valid()

    def is_valid(self):
        self.__correct_chat_id()
        self.__correct_network()
        self.__correct_inputs()
        self.__correct_outputs()

    def __correct_chat_id(self):
        if isinstance(self.chatID, str) and not self.chatID.isdigit():
            raise ValidationError('The chatID must be an integer!')
        if not UserModel.objects.get(self.chatID):
            raise ValidationError('This chatID is not in the database!')

    def __correct_network(self):
        if not NetworkModel.objects.filter(network=self.network.split("_")[0])[0]:
            raise ValidationError('This network is not in the database!')

    def __correct_inputs(self):
        if self.inputs is None or (isinstance(self.inputs, list) and len(self.inputs) == 0):
            self.inputs = [WalletModel.objects.filter(network=self.network, user_id=self.chatID)[0]]
        if self.inputs is not None and isinstance(self.inputs, list) and len(self.inputs) >= 1:
            for address in self.inputs:
                if not WalletModel.objects.filter(network=self.network, user_id=self.chatID, address=address)[0]:
                    raise ValidationError('This address was not found in the database, or does not belong to this chatID!')

    def __correct_outputs(self):
        if isinstance(self.outputs, list) and len(self.outputs) >= 1 and not isinstance(self.outputs[0], dict):
            raise ValidationError('The data should look like this: dict in list!')
        if isinstance(self.outputs, list) and len(self.outputs) >= 1:
            for output in self.outputs:
                if output.get("address") is None or output.get("amount") is None:
                    raise ValidationError('The data should look like this: [{"address": "...", "amount": "..."}, ...]!')
                elif self.MAX_AMOUNT <= decimals.create_decimal(output.get("amount")) <= self.MIN_AMOUNT:
                    raise ValidationError(
                        f'The amount must be greater than {self.MIN_AMOUNT} and not exceed {self.MAX_AMOUNT}!'
                    )

# Response
class ResponseSendTransactionModel:
    """Type of output data"""
    def __init__(self, message: bool = True):
        self.message: bool = message

# <<<========================================>>> Send transaction <<<================================================>>>

class SendTransaction(BaseApiModel):
    """
    This class sending transactions in a certain crypto network.
    """
    QUEUE = Config.RABBITMQ_QUEUE_FOR_BALANCER

    @staticmethod
    def send_transaction(body: BodySendTransactionModel) -> ResponseSendTransactionModel:
        """Send transaction"""
        from_address, to_address = Utils.get_inputs_and_outputs_for_text(inputs=body.inputs, outputs=body.outputs)
        network, token = body.network.split("_")
        try:
            Sender.send_message_to_bot(
                chat_id=body.chatID,
                network=body.network,
                fromAddress=from_address,
                to_address=to_address,
                fee=body.fee,
                amount=Utils.get_amount(outputs=body.outputs),
                status=0,
                method="CREATE",
            )
        except Exception as error:
            logger.error(f"ERROR: {error}")
            Sender.send_message_to_checker(
                text=f"{error}",
                method="INFO_CHECKER"
            )






    @staticmethod
    def is_found(chat_id: TG_CHAT_ID, network: FULL_NETWORK) -> bool:
        """If the transaction is in the repository"""
        return transaction_repository.get_transaction(
            chat_id=chat_id,
            network=network
        ) is not None

send_transaction = SendTransaction