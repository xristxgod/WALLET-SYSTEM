from typing import Optional, List, Dict
import decimal

from rest_framework import serializers

from api.utils.types import CRYPRO_ADDRESS, CRYPTO_MNEMONIC_WORDS, FULL_NETWORK, NETWORK, TG_CHAT_ID

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
    chatID: TG_CHAT_ID = serializers.IntegerField()
    network: FULL_NETWORK = serializers.CharField(max_length=10)
    inputs: Optional[List[CRYPRO_ADDRESS]] = serializers.ListField(default=[])
    outputs: List[Dict[CRYPRO_ADDRESS, str]] = serializers.ListField()
    fee: Optional[decimal.Decimal] = serializers.DecimalField(default=0, decimal_places=10, max_digits=18)

# Response
class ResponserCreateTransactionSerializer(serializers.Serializer):
    fee: decimal.Decimal = serializers.DecimalField(default=0, decimal_places=10, max_digits=18)

class ResponserSendTransactionSerializer(serializers.Serializer):
    message: Optional[bool] = serializers.BooleanField(default=True)

# <<<======================================>>> Create wallet <<<=====================================================>>>
# Body
class BodyCreateWalletSerializer(serializers.Serializer):
    chatID: TG_CHAT_ID = serializers.IntegerField()
    network: NETWORK = serializers.CharField(max_length=10)
    passphrase: Optional[str] = serializers.CharField(max_length=20, default=None)
    mnemonicWords: Optional[CRYPTO_MNEMONIC_WORDS] = serializers.CharField(max_length=255, default=None)

# Response
class ResponserCreateWalletSerializer(serializers.Serializer):
    message: Optional[bool] = serializers.BooleanField(default=True)

