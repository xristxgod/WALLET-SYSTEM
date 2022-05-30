from django.contrib import admin

from api.models import (
    UserModel, TokenModel, NetworkModel, WalletModel,
    TransactionStatusModel, TransactionModel, BalanceModel
)

class UserModelAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "is_admin")
    list_display_links = ("id", "username", "is_admin")
    search_fields = ("id", "username", "is_admin")
    list_filter = ("id", "username", "is_admin")

class TokenModelAdmin(admin.ModelAdmin):
    list_display = ("network", "token")
    list_display_links = ("network", "token")
    search_fields = ("network", "token")
    list_filter = ("network", "token")

class NetworkModelAdmin(admin.ModelAdmin):
    list_display = ("network",)
    list_display_links = ("network",)
    search_fields = ("network",)
    list_filter = ("network",)

class WalletModelAdmin(admin.ModelAdmin):
    list_display = ("id", "network", "address", "user_id")
    list_display_links = ("id", "network", "address", "user_id")
    search_fields = ("id", "network", "user_id")
    list_filter = ("id", "network", "user_id")

class TransactionStatusModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("id", "title")
    list_filter = ("id", "title")

class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ("id", "network", "token", "transaction_hash", "amount", "status", "user_id")
    list_display_links = ("id", "network", "token", "transaction_hash", "amount", "status", "user_id")
    search_fields = ("id", "network", "token", "user_id", "status")
    list_filter = ("id", "network", "token", "user_id", "status")

class BalanceModelAdmin(admin.ModelAdmin):
    list_display = ("balance", "user_id", "network", "token")
    list_display_links = ("balance", "user_id", "network", "token")
    search_fields = ("balance", "user_id", "network", "token")
    list_filter = ("balance", "user_id", "network", "token")

admin.site.register(UserModel, UserModelAdmin)
admin.site.register(TokenModel, TokenModelAdmin)
admin.site.register(NetworkModel, NetworkModelAdmin)
admin.site.register(WalletModel, WalletModelAdmin)
admin.site.register(TransactionStatusModel, TransactionStatusModelAdmin)
admin.site.register(TransactionModel, TransactionModelAdmin)
admin.site.register(BalanceModel, BalanceModelAdmin)
