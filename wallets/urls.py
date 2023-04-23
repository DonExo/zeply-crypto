from django.urls import path

from wallets import views

app_name = "wallets"

urlpatterns = [
    path('addresses/', views.CryptoAddressListRetrieveView.as_view(), name='crypto_addresses'),
    path('addresses/<int:id>/', views.CryptoAddressListRetrieveView.as_view(), name='crypto_address_detail'),
    path('addresses/create/', views.CryptoAddressCreateView.as_view(), name='crypto_address_create'),
]