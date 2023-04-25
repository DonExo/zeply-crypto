import time

from bitcoinlib.wallets import wallet_create_or_open
from .utils import hash_data
from eth_account import Account
from rest_framework import serializers

from .models import CryptoAddress, CryptoWallet


# List Serializer
class CryptoAddressListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoAddress
        fields = ["id", "type", "address", "created_at"]


# Create serializer
class CryptoAddressCreateSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    mnemonic = serializers.CharField(write_only=True)

    class Meta:
        model = CryptoAddress
        fields = ["id", "type", "mnemonic", "address", "created_at"]
        read_only_fields = ["address"]

    def create(self, validated_data):
        crypto_type = validated_data["type"]
        crypto_type = crypto_type.upper()
        mnemonic = validated_data.get("mnemonic")

        match crypto_type:
            case CryptoAddress.CHOICE_BTC | CryptoAddress.CHOICE_LTC:
                crypto_address = self._generate_bitcoin_litecoin_address(crypto_type, mnemonic)
            case CryptoAddress.CHOICE_ETH:
                crypto_address = self._generate_ethereum_address(mnemonic)
            # Add here more 'cases' for different cryptocurrencies
            case _:
                raise serializers.ValidationError(
                    {"error": "Invalid cryptocurrency ticker provided."}
                )
        return crypto_address

    @staticmethod
    def _generate_bitcoin_litecoin_address(crypto_type: str, mnemonic: str) -> CryptoAddress:
        """
        Utility function that creates a Bitcoin or Bitcoin-based address.
        Uses the 'bitcoinlib' library that has support for Bitcoin, Litecoin and other bitcoin-based currencies.
        It created (almost) unique wallet_name by using timestamp as part of the wallet name.
        :param crypto_type: The type of cryptocurrency.
        :param mnemonic: The user's mnemonic phrase, or Master seed.
        :return: The newly created internal CryptoAddress object.
        """
        network = "testnet" if crypto_type == "BTC" else "litecoin_testnet"
        hashed_mnemonic = hash_data(mnemonic)
        existing_accounts = CryptoWallet.objects.filter(mnemonic=hashed_mnemonic)
        # First check if there is an existing Wallet with the given (hashed) mnemonic
        if existing_accounts.exists():
            crypto_wallet = existing_accounts.first()
            # if there is, "open" the bitcoinlib wallet by its name
            bitcoinlib_wallet = wallet_create_or_open(name=crypto_wallet.wallet_name)
            address = bitcoinlib_wallet.get_key().address
        else:
            # If there isn't, create a new bitcoinlib wallet and CryptoWallet object, along with a valid address
            unique_name = f"wallet_{network}_" + str(time.time())
            crypto_wallet = CryptoWallet.objects.create(wallet_name=unique_name, mnemonic=hashed_mnemonic)
            bitcoinlib_wallet = wallet_create_or_open(name=unique_name, keys=mnemonic, network=network)
            address = bitcoinlib_wallet.new_key().address

        # Create an address, assign it to a wallet and a type
        crypto_address = CryptoAddress.objects.create(type=crypto_type, address=address, wallet=crypto_wallet)
        return crypto_address

    @staticmethod
    def _generate_ethereum_address(mnemonic: str) -> CryptoAddress:
        """
        Utility function that creates a Ethereum address.
        It first creates a 32-bit hex random token then generates an Ethereum account of it.
        Uses the 'web3' and 'eth-account' library that has support for Ethereum.
        :param mnemonic: The user's mnemonic phrase, or Master seed.
        :return: The newly created internal CryptoAddress object.
        """

        hashed_mnemonic = hash_data(mnemonic)
        existing_accounts = CryptoWallet.objects.filter(mnemonic=hashed_mnemonic)
        # First check if there is an existing Wallet with the given (hashed) mnemonic
        if existing_accounts.exists():
            crypto_wallet = existing_accounts.first()
        else:
            unique_name = "wallet_eth_" + str(time.time())
            crypto_wallet = CryptoWallet.objects.create(wallet_name=unique_name, mnemonic=hashed_mnemonic)
        Account.enable_unaudited_hdwallet_features()
        eth_wallet = Account.create()
        crypto_address = CryptoAddress.objects.create(type="ETH", address=eth_wallet.address, wallet=crypto_wallet)

        return crypto_address


# BONUS: Sorting functionality serializers
class CryptoAddressNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoAddress
        fields = ["id", "address", "created_at"]


class CryptoAddressListGroupedByTypeSerializer(serializers.Serializer):
    type = serializers.CharField()
    addresses = CryptoAddressNestedSerializer(many=True)
