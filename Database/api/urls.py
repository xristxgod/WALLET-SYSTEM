from django.urls import path
from rest_framework import routers

from api.api import UserModelViewSet

router = routers.DefaultRouter()

router.register("api/user", UserModelViewSet, "user")

urlpatterns = router.urls