from django.db import models
from django.utils.translation import gettext_lazy as _


class CryptoAddress(models.Model):
    CHOICE_BTC = "BTC"
    CHOICE_ETH = "ETH"
    CRYPTO_CHOICES = (
        (CHOICE_BTC, 'Bitcoin'),
        (CHOICE_ETH, 'Ethereum'),
        # Add here more choices as needed
    )

    type = models.CharField(_("Crypto currency type"), max_length=10, choices=CRYPTO_CHOICES)
    address = models.CharField(_("Crypto currency address"), max_length=128)

    def __str__(self):
        return f"({self.type}) {self.address}"
