from rest_framework import viewsets, permissions

from api.models import UserModel
from api.serializers import UserModelSerializer

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserModelSerializer