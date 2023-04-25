from django.db import models
from django.utils.translation import gettext_lazy as _


class CryptoWallet(models.Model):
    mnemonic = models.CharField(max_length=256)
    wallet_name = models.CharField(_("Wallet name"), max_length=128)

    def __str__(self):
        return self.wallet_name  # pragma: no cover


class CryptoAddress(models.Model):
    CHOICE_BTC = "BTC"
    CHOICE_ETH = "ETH"
    CHOICE_LTC = "LTC"

    CRYPTO_CHOICES = (
        (CHOICE_BTC, "Bitcoin"),
        (CHOICE_ETH, "Ethereum"),
        (CHOICE_LTC, "Litecoin"),
        # Add here more choices as needed
    )

    # It was explicitly asked for the Primary Key to be an Integer ID, otherwise something like UUID is smarter choice.
    id = models.AutoField(primary_key=True)  # Make it explicit
    type = models.CharField(
        _("Crypto currency type"), max_length=10, choices=CRYPTO_CHOICES
    )
    address = models.CharField(_("Crypto currency address"), max_length=128)
    wallet = models.ForeignKey(CryptoWallet, on_delete=models.CASCADE, related_name="addresses", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.type}) {self.address}"  # pragma: no cover
