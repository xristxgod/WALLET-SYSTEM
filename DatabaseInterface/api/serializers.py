from rest_framework import serializers

class BodyCoinToCoinSerializer(serializers.Serializer):
    coin = serializers.CharField(max_length=10)
    toCoin = serializers.CharField(max_length=10, default=None)

class ResponseCoinToCoinSerializer(serializers.Serializer):
    price = serializers.DecimalField(default=0, decimal_places=10, max_digits=18)
