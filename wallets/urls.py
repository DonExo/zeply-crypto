from django.contrib import admin
from django.urls import path, include

from wallets.views import CryptoAddressView

app_name = "wallets"

urlpatterns = [
    path('generate/<str:crypto_type>', CryptoAddressView.as_view(), name="generate"),
    # path('list/', CryptoAddressView.as_view(), name="generate"),
    # path('get/<>', CryptoAddressView.as_view(), name="generate"),
]