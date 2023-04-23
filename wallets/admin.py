from django.contrib import admin

from wallets.models import CryptoAddress


@admin.register(CryptoAddress)
class CryptoAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "type", "address", "created_at"]
    list_filter = ("type", )