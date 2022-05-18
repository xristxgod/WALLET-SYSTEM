from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.create_transaction import BodyCreateTransactionModel, create_transaction
from api.services.send_transaction import BodySendTransactionModel, send_transaction
from api.services.coin_to_coin import BodyCoinToCoinModel,  coin_to_coin

class CoinToCoinAPIView(APIView):
    """Coin to coin api view"""
    def post(self, request) -> Response:
        coin_to_coin.decode(data=request.data)
        data = coin_to_coin.get_price(body=BodyCoinToCoinModel(**request.data))
        return Response(coin_to_coin.encode(data=data))

class CreateTransactionAPIView(APIView):
    """Create transaction api view"""
    def post(self, request) -> Response:
        create_transaction.decode(data=request.data)
        data = create_transaction.create_transaction(body=BodyCreateTransactionModel(is_check=True, **request.data))
        return Response(create_transaction.encode(data=data))

class SendTransactionAPIView(APIView):
    """Send transaction api view"""
    def post(self, request) -> Response:
        send_transaction.decode(data=request.data)
        if send_transaction.is_found(chat_id=request.data.get('chatID'), network=request.data.get('network')):
            data = send_transaction.send_transaction(body=BodySendTransactionModel(is_check=False, **request.data))
        else:
            data = send_transaction.send_transaction(body=BodySendTransactionModel(is_check=True, **request.data))
        return Response(send_transaction.encode(data=data))

class CreateWalletAPIView(APIView):
    pass