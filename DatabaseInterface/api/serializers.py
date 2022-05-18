from typing import Optional, List, Dict
import decimal

from rest_framework import serializers

# <<<======================================>>> Coin to coin <<<======================================================>>>
# Body
class BodyCoinToCoinSerializer(serializers.Serializer):
    coin: str = serializers.CharField(max_length=10)
    toCoin = serializers.CharField(max_length=10, default=None)

# Response
class ResponseCoinToCoinSerializer(serializers.Serializer):
    price: decimal.Decimal = serializers.DecimalField(default=0, decimal_places=10, max_digits=18)

# <<<======================================>>> Create/send transaction <<<===========================================>>>
# Body
class BodyTransactionSerializer(serializers.Serializer):
    chatID: int = serializers.IntegerField()
    network: str = serializers.CharField(max_length=10)
    inputs: Optional[List[str]] = serializers.ListField(default=[])
    outputs: List[Dict[str, str]] = serializers.ListField()

# Response
class ResponserCreateTransactionSerializer(serializers.Serializer):
    fee: decimal.Decimal = serializers.DecimalField(default=0, decimal_places=10, max_digits=18)

class ResponserSendTransactionSerializer(serializers.Serializer):
    message: Optional[bool] = serializers.BooleanField(default=True)