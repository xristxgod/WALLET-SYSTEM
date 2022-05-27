import uuid
import decimal
from typing import Optional, List, Dict

from rest_framework.exceptions import ValidationError

from api.models import UserModel, NetworkModel, WalletModel, TransactionModel, TokenModel, TransactionStatusModel
from api.serializers import BodyTransactionSerializer, ResponserSendTransactionSerializer
from api.services.__init__ import BaseApiModel, transaction_repository
from api.services.external.sender import Sender
from api.services.external.queue import Queue
from api.utils.types import CRYPRO_ADDRESS, FULL_NETWORK, TG_CHAT_ID
from api.utils.utils import Utils
from config import Config, decimals, logger

QUEUE = Config.RABBITMQ_QUEUE_FOR_BALANCER

# Body
class BodySendTransactionModel:
    """Type of input data"""
    MIN_AMOUNT = decimals.create_decimal(0)
    MAX_AMOUNT = decimals.create_decimal(1000000000000000)

    NETWORK_OBJECT: object

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
        self.network: FULL_NETWORK = self.get_network(network.upper())
        self.inputs: List[CRYPRO_ADDRESS] = inputs if inputs is not None else self.get_inputs()
        self.outputs: List[Dict[CRYPRO_ADDRESS, str]] = outputs
        self.fee: decimal.Decimal = fee
        if is_check:
            self.is_valid()

    def get_inputs(self) -> List[CRYPRO_ADDRESS]:
        return [WalletModel.objects.get(network=self.NETWORK_OBJECT, user_id=self.chatID).address]

    def get_network(self, network: str) -> FULL_NETWORK:
        try:
            self.NETWORK_OBJECT = NetworkModel.objects.get(network=network.split("-")[0])
        except Exception:
            raise ValidationError('This network is not in the database!')
        return network

    def is_valid(self):
        self.__correct_chat_id()
        self.__correct_inputs()
        self.__correct_outputs()

    def __correct_chat_id(self):
        if isinstance(self.chatID, str) and not self.chatID.isdigit():
            raise ValidationError('The chatID must be an integer!')
        if len(UserModel.objects.filter(pk=self.chatID)) == 0:
            raise ValidationError('This chatID is not in the database!')

    def __correct_inputs(self):
        if self.inputs is None or (isinstance(self.inputs, list) and len(self.inputs) == 0):
            self.inputs = [WalletModel.objects.get(network=self.NETWORK_OBJECT, user_id=self.chatID).address]
        if self.inputs is not None and isinstance(self.inputs, list) and len(self.inputs) >= 1:
            for address in self.inputs:
                if not WalletModel.objects.filter(network=self.NETWORK_OBJECT, user_id=self.chatID, address=address):
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
    @staticmethod
    def send_to_bot_alert(network: FULL_NETWORK, amount: decimal.Decimal, body: BodySendTransactionModel) -> Optional:
        """Send to bot alert"""
        try:
            Sender.send_message_to_bot(
                chat_id=body.chatID,
                network=network,
                inputs=Utils.get_inputs(inputs=body.inputs, amount=amount),
                outputs=body.outputs,
                fee=body.fee,
                amount=amount,
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
    def send_transaction(body: BodySendTransactionModel) -> ResponseSendTransactionModel:
        """Send transaction"""
        temporary_transaction_hash = uuid.uuid4().hex
        network, token = body.network.split("-")
        amount = Utils.get_amount(body.outputs)
        # Send to bot alert => bot main
        SendTransaction.send_to_bot_alert(network=body.network, amount=amount, body=body)

        transaction_repository.remove_transaction(chat_id=body.chatID, network=body.network)

        transaction = TransactionModel(
            network=NetworkModel.objects.get(network=network.split("-")[0]),
            time=Utils.get_timestamp_now(),
            transaction_hash=temporary_transaction_hash,
            fee=body.fee,
            amount=amount,
            inputs=Utils.get_correct_inputs(inputs=body.inputs, amount=amount),
            outputs=body.outputs,
            token=TokenModel.objects.get(
                token=token.upper(), network=NetworkModel.objects.get(network=network.split("-")[0])
            ),
            status=TransactionStatusModel.objects.get(title="PROCESSING"),
            user_id=UserModel.objects.get(pk=body.chatID)
        )
        transaction.save()
        # Send to balancer
        status = Queue.send_message(
            queue_name=QUEUE,
            message={
                "chatID": body.chatID,
                "temporary_transaction_hash": temporary_transaction_hash,
                "network": network,
                "token": token,
                "fee": body.fee,
                "inputs": body.inputs,
                "outputs": body.outputs
            }
        )
        return ResponseSendTransactionModel(
            message=status
        )

    @staticmethod
    def is_found(chat_id: TG_CHAT_ID, network: FULL_NETWORK) -> bool:
        """If the transaction is in the repository"""
        return transaction_repository.get_transaction(
            chat_id=chat_id,
            network=network
        ) is not None

    @staticmethod
    def encode(data: ResponseSendTransactionModel) -> ResponserSendTransactionSerializer:
        """Generates data for the response"""
        return ResponserSendTransactionSerializer(data).data

    @staticmethod
    def decode(data) -> Optional:
        """Checks the input data"""
        serializer = BodyTransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)

send_transaction = SendTransaction