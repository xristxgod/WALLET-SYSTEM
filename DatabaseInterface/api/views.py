from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render

class CoinToCoin(APIView):
    def post(self, request):
        return Response({"price": "0.001", "coin": request.data['coin']})