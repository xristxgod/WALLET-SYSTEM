from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.coin_to_coin import BodyCoinToCoinModel, coin_to_coin

class CoinToCoinAPIView(APIView):
    """Coin to coin api view"""
    def post(self, request):
        coin_to_coin.decode(data=request.data)
        data = coin_to_coin.get_price(body=BodyCoinToCoinModel(**request.data))
        return Response(coin_to_coin.encode(data=data))