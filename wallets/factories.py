import factory

from .models import CryptoAddress, CryptoWallet


class CryptoWalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CryptoWallet

    wallet_name = factory.Sequence(lambda n: f"Wallet name {n}")
    mnemonic = factory.Faker('text', max_nb_chars=256)


def get_single_wallet():
    single_wallet, _ = CryptoWallet.objects.get_or_create(wallet_name="Single Wallet")
    return single_wallet


class CryptoAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CryptoAddress

    type = factory.Iterator(["BTC", "ETH", "LTC"])
    address = factory.Sequence(lambda n: f"Generated crypto address {n}")
    wallet = factory.LazyAttribute(lambda o: get_single_wallet())
