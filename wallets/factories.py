import factory
from .models import CryptoAddress


class CryptoAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CryptoAddress

    type = factory.Iterator(['BTC', 'ETH', 'LTC'])
    address = factory.Sequence(lambda n: f"Generated crypto address {n}")
