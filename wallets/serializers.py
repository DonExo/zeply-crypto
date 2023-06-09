import secrets
import time

from bitcoinlib.wallets import Wallet
from eth_account import Account
from rest_framework import serializers

from .models import CryptoAddress


# List Serializer
class CryptoAddressListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoAddress
        fields = ["id", "type", "address", "created_at"]


# Create serializer
class CryptoAddressCreateSerializer(serializers.ModelSerializer):
    type = serializers.CharField()

    class Meta:
        model = CryptoAddress
        fields = ["id", "type", "address", "created_at"]
        read_only_fields = ["address"]

    def create(self, validated_data):
        crypto_type = validated_data["type"]
        crypto_type = crypto_type.upper()

        match crypto_type:
            case CryptoAddress.CHOICE_BTC | CryptoAddress.CHOICE_LTC:
                crypto_address = self._generate_bitcoin_litecoin_address(crypto_type)
            case CryptoAddress.CHOICE_ETH:
                crypto_address = self._generate_ethereum_address()
            # Add here more 'cases' for different cryptocurrencies
            case _:
                raise serializers.ValidationError(
                    {"error": "Invalid cryptocurrency ticker provided."}
                )
        return crypto_address

    @staticmethod
    def _generate_bitcoin_litecoin_address(crypto_type: str) -> CryptoAddress:
        """
        Utility function that creates a Bitcoin or Bitcoin-based address.
        Uses the 'bitcoinlib' library that has support for Bitcoin, Litecoin and other bitcoin-based currencies.
        It created (almost) unique wallet_name by using timestamp as part of the wallet name.
        :param crypto_type: The type of cryptocurrency.
        :return: The newly created internal CryptoAddress object.
        """
        network = "testnet" if crypto_type == "BTC" else "litecoin_testnet"
        unique_name = "wallet_name_" + str(time.time())
        wallet = Wallet.create(unique_name, network=network)
        address = wallet.new_key().address
        crypto_address = CryptoAddress.objects.create(type=crypto_type, address=address)
        return crypto_address

    @staticmethod
    def _generate_ethereum_address() -> CryptoAddress:
        """
        Utility function that creates a Ethereum address.
        It first creates a 32-bit hex random token then generates an Ethereum account of it.
        Uses the 'web3' and 'eth-account' library that has support for Ethereum.
        :return: The newly created internal CryptoAddress object.
        """
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        account = Account.from_key(private_key)
        crypto_address = CryptoAddress.objects.create(
            type="ETH", address=account.address
        )
        return crypto_address


# BONUS: Sorting functionality serializers
class CryptoAddressNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoAddress
        fields = ["id", "address", "created_at"]


class CryptoAddressListGroupedByTypeSerializer(serializers.Serializer):
    type = serializers.CharField()
    addresses = CryptoAddressNestedSerializer(many=True)
