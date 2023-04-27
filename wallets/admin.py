from django.contrib import admin

from wallets.models import CryptoAddress, CryptoWallet


@admin.register(CryptoAddress)
class CryptoAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "type", "address", "created_at", "get_wallet"]
    list_filter = ("type",)

    def get_wallet(self, obj):
        if obj.wallet:
            return obj.wallet.wallet_name
        return None


@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ["wallet_name", "mnemonic"]
