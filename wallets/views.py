import time
import secrets

from django.http import JsonResponse
from django.views import View

from bitcoinlib.wallets import Wallet
from eth_account import Account

from wallets.models import CryptoAddress


class CryptoAddressView(View):
    """

    """
    def post(self, request, crypto_type, *args, **kwargs):
        if not crypto_type:
            return JsonResponse({"message": "You need to provide cryptocurrency ticker."}, status=400)
        match crypto_type.upper():
            case CryptoAddress.CHOICE_BTC:
                return self._generate_bitcoin_address()
            case CryptoAddress.CHOICE_ETH:
                return self._generate_ethereum_address()
            # Add here more 'cases' for different cryptocurrencies
            case _:
                return JsonResponse({"message": "Invalid cryptocurrency marker."}, status=400)

    def _generate_bitcoin_address(self):
        unique_name = "wallet_name_" + str(time.time())
        wallet = Wallet.create(unique_name,  network="testnet")
        address = wallet.new_key().address
        CryptoAddress.objects.create(type="BTC", address=address)
        blockchain_test_url = "https://www.blockchain.com/explorer/addresses/btc-testnet/" + address
        return JsonResponse({"message": {"wallet_name": wallet.name, "address": address, "test_url": blockchain_test_url}}, status=200)

    def _generate_ethereum_address(self):
        priv = secrets.token_hex(32)
        priv_key = "0x" + priv
        account = Account.from_key(priv_key)
        CryptoAddress.objects.create(type="ETH", address=account.address)
        # account = Account.from_mnemonic('some many words')
        blockchain_test_url = "https://etherscan.io/address/" + account.address
        return JsonResponse({"message": {"address": account.address, "test_url": blockchain_test_url}}, status=200)

