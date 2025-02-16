from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import BuyMerchView, InfoView, SendCoinsView

urlpatterns = [
    path("auth/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("info/", InfoView.as_view(), name="info"),
    path("buy/<str:item>/", BuyMerchView.as_view(), name="buy"),
    path("sendCoin/", SendCoinsView.as_view(), name="send_coin"),
]
