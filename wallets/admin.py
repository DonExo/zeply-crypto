from django.contrib import admin

from wallets.models import CryptoAddress

@admin.register(CryptoAddress)
class CryptoAddressAdmin(admin.ModelAdmin):
    pass