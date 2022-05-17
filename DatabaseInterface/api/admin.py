from django.contrib import admin

from api.models import UserModel, TokenModel, NetworkModel, WalletModel, TransactionStatusModel, TransactionModel

class UserModelAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "is_admin")
    list_display_links = ("id", "username", "is_admin")
    search_fields = ("id", "username", "is_admin")
    list_filter = ("id", "username", "is_admin")

class TokenModelAdmin(admin.ModelAdmin):
    list_display = ("id", "network", "token")
    list_display_links = ("id", "network", "token")
    search_fields = ("id", "network", "token")
    list_filter = ("id", "network", "token")

class NetworkModelAdmin(admin.ModelAdmin):
    list_display = ("id", "network")
    list_display_links = ("id", "network")
    search_fields = ("id", "network")
    list_filter = ("id", "network")

class WalletModelAdmin(admin.ModelAdmin):
    list_display = ("id", "network", "address", "user_id", "last_balance")
    list_display_links = ("id", "network", "address", "user_id", "last_balance")
    search_fields = ("id", "network", "user_id")
    list_filter = ("id", "network", "user_id")

class TransactionStatusModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status_number")
    list_display_links = ("id", "title", "status_number")
    search_fields = ("id", "title", "status_number")
    list_filter = ("id", "title", "status_number")

class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ("id", "network", "token", "transaction_hash", "amount", "status", "user_id")
    list_display_links = ("id", "network", "token", "transaction_hash", "amount", "status", "user_id")
    search_fields = ("id", "network", "token", "user_id", "status")
    list_filter = ("id", "network", "token", "user_id", "status")

admin.site.register(UserModel, UserModelAdmin)
admin.site.register(TokenModel, TokenModelAdmin)
admin.site.register(NetworkModel, NetworkModelAdmin)
admin.site.register(WalletModel, WalletModelAdmin)
admin.site.register(TransactionStatusModel, TransactionStatusModelAdmin)
admin.site.register(TransactionModel, TransactionModelAdmin)
