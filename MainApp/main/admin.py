from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import UserModel
from main.models import NetworkModel, TokenModel, TransactionStatusModel
from main.models import WalletModel, BalanceModel
from main.models import TransactionModel

@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    model = UserModel
    list_display = (*UserAdmin.list_display, "show_display")
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            "Photo",
            {
                "fields": (
                    "profile_picture",
                )
            }
        ),
        (
            "Telegram info",
            {
                "fields": (
                    "telegram_chat_id",
                )
            }
        ),
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Photo",
            {
                "fields": (
                    "profile_picture",
                    "show_field"
                )
            }
        ),
        (
            "Telegram info",
            {
                "fields": (
                    "telegram_chat_id",
                )
            }
        )
    )
    readonly_fields = (*UserAdmin.readonly_fields, 'show_field',)


# <<<=======================================>>> Base Models <<<======================================================>>>


@admin.register(NetworkModel)
class NetworkModelAdmin(admin.ModelAdmin):
    fields = ("network", "blockchain_url", "description", "logo", "show_field")
    list_display = ("network", "blockchain_url", "show_display")
    list_display_links = ("network", "blockchain_url")
    search_fields = ("network",)
    list_filter = ("network",)
    readonly_fields = ('show_field',)


@admin.register(TokenModel)
class TokenModelAdmin(admin.ModelAdmin):
    fields = ("token", "network", "decimals", "address", "description", "token_info", "logo", "show_field")
    list_display = ("token", "network", "address", "show_display")
    list_display_links = ("token", "network")
    search_fields = ("token", "network", "decimals", "address")
    list_filter = ("token", "network", "decimals", "address")
    readonly_fields = ('show_field',)


@admin.register(TransactionStatusModel)
class TransactionStatusModelAdmin(admin.ModelAdmin):
    fields = ("id", "title", "description", "logo", "show_field")
    list_display = ("id", "title", "show_display")
    list_display_links = ("id", "title")
    search_fields = ("id", "title")
    list_filter = ("id", "title")
    readonly_fields = ('show_field',)


# <<<=======================================>>> Wallet Models <<<====================================================>>>


@admin.register(WalletModel)
class WalletModelAdmin(admin.ModelAdmin):
    list_display = ("address", "network", "user_id")
    list_display_links = ("address", "network", "user_id")
    search_fields = ("address", "network", "user_id")
    list_filter = ("address", "network", "user_id")


@admin.register(BalanceModel)
class BalanceModelAdmin(admin.ModelAdmin):
    list_display = ("balance", "wallet", "network", "token", "user_id")
    list_display_links = ("balance", "wallet", "network", "token", "user_id")
    search_fields = ("wallet", "network", "token", "user_id")
    list_filter = ("wallet", "network", "token", "user_id")


# <<<=======================================>>> Transaction Models <<<===============================================>>>


@admin.register(TransactionModel)
class TransactionModelAdmin(admin.ModelAdmin):
    fields = ("time", "transaction_hash", "fee", "amount", "inputs", "outputs", "status", "network", "token", "user_id")
    list_display = ("correct_datetime", "transaction_hash", "network", "token", "user_id", "show_display")
    list_display_links = ("transaction_hash", "network", "token", "user_id")
    search_fields = ("time", "transaction_hash", "network", "token", "user_id", "status")
    list_filter = ("time", "transaction_hash", "network", "token", "user_id", "status")
    readonly_fields = ('show_field',)
