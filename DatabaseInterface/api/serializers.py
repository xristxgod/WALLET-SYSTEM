from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

class CoinToCoinSerializer(serializers.Serializer):
    price = serializers.DecimalField(default=0)