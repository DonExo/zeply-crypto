from django.http import HttpResponse, JsonResponse
from django.views import View

from bitcoinlib.wallets import Wallet
import time
from eth_account import Account
import secrets

accepted_crypto_types = ["BTC", "ETH"]


class CryptoAddressView(View):
    """

    """
    def post(self, request, crypto_type, *args, **kwargs):
        if not crypto_type:
            return HttpResponse("NOT GOOD", status=400)
        match crypto_type.upper():
            case "BTC":
                return self._generate_bitcoin_address()
            case "ETH":
                return self._generate_etherium_address()
            case _:
                return JsonResponse({"message": "Invalid Crypto marker."}, status=400)

    def _generate_bitcoin_address(self):
        unique_name = "wallet_name_" + str(time.time())
        wallet = Wallet.create(unique_name,  network="testnet")
        address = wallet.new_key().address
        blockchain_test_url = "https://www.blockchain.com/explorer/addresses/btc-testnet/" + address
        return JsonResponse({"message": {"wallet_name": wallet.name, "address": address, "test_url": blockchain_test_url}}, status=200)

    def _generate_etherium_address(self):
        priv = secrets.token_hex(32)
        priv_key = "0x" + priv
        account = Account.from_key(priv_key)
        # account = Account.from_mnemonic('some many words')
        blockchain_test_url = "https://etherscan.io/address/" + account.address
        return JsonResponse({"message": {"address": account.address, "test_url": blockchain_test_url}}, status=200)

