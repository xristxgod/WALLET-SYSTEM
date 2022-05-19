from rest_framework.response import Response
from rest_framework.views import APIView


from api.services.__init__ import transaction_repository
from api.services.create_wallet import BodyCreateWalletModel, create_wallet
from api.services.get_balance import BodyGetBalanaceModel, get_balance
from api.services.create_transaction import BodyCreateTransactionModel, create_transaction
from api.services.send_transaction import BodySendTransactionModel, send_transaction
from api.services.coin_to_coin import BodyCoinToCoinModel, coin_to_coin

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
    """Create wallet api view"""
    def post(self, request) -> Response:
        create_wallet.decode(data=request.data)
        data = create_wallet.create_wallet(body=BodyCreateWalletModel(**request.data))
        return Response(create_wallet.encode(data=data))

class BalanceAPIView(APIView):
    """Get balance api view"""
    def post(self, request) -> Response:
        get_balance.decode(data=request.data)
        data = get_balance.get_balance(body=BodyGetBalanaceModel(**request.data))
        return Response(get_balance.encode(data=data))

# <<<========================================>>> System APIs <<<=====================================================>>>

class GetTransactionRepositoryCacheAPIView(APIView):
    """
    This module returns data from the transaction caching class. Checks its operability!
    """
    def get(self, request) -> Response:
        cache = transaction_repository.transactions
        return Response({
            "repositoryCacheCount": len(cache),
            "repositoryCacheData": cache,
            "message": len(cache) < 15
        })

class APISystemStatusAPIView(APIView):
    """
    This module checks the rest api system status.
    """
    def get(self, request) -> Response:
        return Response({"message": True})

class DatabaseStatusAPIView(APIView):
    """
    This module checks the status of the database.
    """
    def get(self, request) -> Response:
        return Response({"message": True})