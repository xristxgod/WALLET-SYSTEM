from django.urls import path

from sign.views.auth_views import LoginAuthenticationView
from sign.views.auth_views import LoginAuthView

urlpatterns = [
    path("login/", LoginAuthenticationView.as_view(), name="login"),
    path("login/auth/<str:params>", LoginAuthView.as_view(), name="login_auth"),
]
