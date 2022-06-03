import uuid
from datetime import datetime

from django.db import models
from django.template.defaultfilters import truncatechars
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from src.utils.types import CoinHelper
from src.utils.utils import UtilsImage
from src.utils.filters import BaseFilter, ImageFilter, DatetimeFilter
from src.utils.validators import ImageValidators, WalletValidators, TransactionValidators


class UserModel(AbstractUser, ImageFilter):
    """Base user model"""
    telegram_chat_id = models.IntegerField(unique=True, blank=True, null=True, verbose_name="Telegram user ID")
    google_auth_code = models.CharField(unique=True, blank=True, max_length=25, null=True, verbose_name="Google auth code")
    profile_picture = models.ImageField(
        null=True, blank=True,
        verbose_name="Your photo", validators=[ImageValidators.validate_image_expansion],
        upload_to=UtilsImage.image_name_user
    )

    @property
    def show_display(self):
        if self.profile_picture.name:
            return UtilsImage.image_url(image_url=self.profile_picture.url, method="display")
        return "Not photo"

    @property
    def show_field(self):
        if self.profile_picture.name:
            return UtilsImage.image_url(image_url=self.profile_picture.url, method="field")
        return "Not photo"


# <<<=======================================>>> Base Models <<<======================================================>>>


class NetworkModel(models.Model, BaseFilter):
    """Network model - It is used to describe crypto networks!"""
    network: str = models.CharField(primary_key=True, verbose_name="Network name", max_length=15, unique=True)
    logo = models.ImageField(
        blank=True, null=True, verbose_name="Network logo", validators=[
            ImageValidators.validate_logo, ImageValidators.validate_image_expansion
        ], upload_to=UtilsImage.image_name_network
    )
    blockchain_url = models.URLField(blank=True, null=True, verbose_name="Blockchain URL")
    description: str = models.TextField(blank=True, null=True, verbose_name="Network description")

    def __str__(self):
        return f"{self.network}"

    def save(self, *args, **kwargs):
        self.network = self.network.upper()
        super().save(*args, **kwargs)

    @property
    def short_description(self):
        return truncatechars(self.description, 30) if len(self.description) > 30 else "Not description"

    @property
    def show_display(self):
        if self.logo.name:
            return UtilsImage.image_url(image_url=self.logo.url, method="display")
        return "Not logo"

    @property
    def show_field(self):
        if self.logo.name:
            return UtilsImage.image_url(image_url=self.logo.url, method="field")
        return "Not logo"

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Networks'
        db_table = 'network_model'


class TokenModel(models.Model, BaseFilter):
    """Token model - It is used to describe crypto tokens (smart contracts) in the crypto network!"""
    token: str = models.CharField(verbose_name="Token name", max_length=15)
    network: str = models.ForeignKey(
        "NetworkModel", on_delete=models.CASCADE, db_column="network", verbose_name="Network name",
    )
    logo = models.ImageField(
        blank=True, null=True, verbose_name="Token logo", validators=[ImageValidators.validate_logo],
        upload_to=UtilsImage.image_name_token
    )
    decimals = models.IntegerField(verbose_name="Token decimals", validators=[
        MinValueValidator(0), MaxValueValidator(20)
    ])
    address = models.CharField(verbose_name="Token smart contract address", max_length=255, unique=True)
    description: str = models.TextField(blank=True, null=True, verbose_name="Token description")
    token_info = models.JSONField(blank=True, null=True, verbose_name="Token info")

    def __str__(self):
        return f"{self.network}-{self.token}"

    @property
    def short_description(self):
        return truncatechars(self.description, 30) if len(self.description) > 30 else "Not description"

    def save(self, *args, **kwargs):
        self.token = self.token.upper()
        super().save(*args, **kwargs)

    @property
    def show_display(self):
        if self.logo.name:
            return UtilsImage.image_url(image_url=self.logo.url, method="display")
        return "Not logo"

    @property
    def show_field(self):
        if self.logo.name:
            return UtilsImage.image_url(image_url=self.logo.url, method="field")
        return "Not logo"

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        db_table = 'token_model'


class TransactionStatusModel(models.Model, BaseFilter):
    """Transaction status model - It is used to describe transaction statuses."""
    id = models.IntegerField(
        unique=True, primary_key=True, validators=[MinValueValidator(-1), MaxValueValidator(4)]
    )
    logo = models.ImageField(
        blank=True, null=True, verbose_name="Status logo", validators=[ImageValidators.validate_logo],
        upload_to=UtilsImage.image_transaction_status
    )
    title: str = models.CharField(max_length=30, verbose_name="Status name", unique=True)
    description: str = models.TextField(blank=True, null=True, verbose_name="Status description")

    def __str__(self):
        return f"{self.title}"

    @property
    def short_description(self):
        return truncatechars(self.description, 30) if len(self.description) > 30 else "Not description"

    def save(self, *args, **kwargs):
        self.title = self.title.upper()
        super().save(*args, **kwargs)

    @property
    def show_display(self):
        if self.logo.name:
            return UtilsImage.image_url(image_url=self.logo.url, method="display")
        return "Not logo"

    @property
    def show_field(self):
        if self.logo.name:
            return UtilsImage.image_url(image_url=self.logo.url, method="field")
        return "Not logo"

    class Meta:
        verbose_name = 'Transaction Status'
        verbose_name_plural = 'Transactions Status'
        db_table = 'transaction_status_model'


# <<<=======================================>>> Wallet Models <<<====================================================>>>


class WalletModel(models.Model):
    """Wallet model - It is used to store users' crypto wallets."""
    address = models.CharField(verbose_name="Wallet address", max_length=255, unique=True)
    private_key = models.CharField(verbose_name="Wallet private key", max_length=255, unique=True)
    public_key = models.CharField(
        verbose_name="Wallet public key", max_length=255, unique=True, blank=True, null=True
    )
    passphrase = models.CharField(
        verbose_name="Wallet passphrase", max_length=25, blank=True, null=True
    )
    mnemonic_phrase = models.CharField(
        verbose_name="Wallet mnemonic phrase", max_length=255, validators=[WalletValidators.validate_mnemonic],
        blank=True, null=True
    )
    network: str = models.ForeignKey(
        "NetworkModel", on_delete=models.CASCADE, db_column="network", verbose_name="Network name",
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="user_id", verbose_name="Owner id"
    )

    def __str__(self):
        return f"{self.user_id}|{self.network}"

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        db_table = 'wallet_model'


class BalanceModel(models.Model):
    """Balance model - It is used to store the balance of users"""
    balance = models.DecimalField(decimal_places=6, max_digits=18, verbose_name="Wallet balance", default=0)
    wallet: WalletModel = models.ForeignKey(
        "WalletModel", on_delete=models.CASCADE, db_column="wallet", verbose_name="Wallet"
    )
    network: NetworkModel = models.ForeignKey(
        "NetworkModel", on_delete=models.CASCADE, db_column="network", verbose_name="Network name",
    )
    token: TokenModel = models.ForeignKey(
        "TokenModel", on_delete=models.CASCADE, db_column="token", verbose_name="Token name", blank=True, null=True
    )
    user_id: UserModel = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="user_id", verbose_name="Owner id"
    )

    def __str__(self):
        return (
            f"{self.user_id}|{self.network.network}-"
            f"{self.token.token if self.token else CoinHelper.get_native_coin(self.network.network)}"
        )

    def save(self, *args, **kwargs):
        if self.network.network != self.token.network:
            pass
        elif self.network.network != self.wallet.network:
            pass
        else:
            super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.token and self.network != self.token.network:
            raise ValidationError(
                {
                    "token": "The token's network must be the same as the network. Network: {} != Token: {}".format(
                        self.network.network, self.token
                    )
                }
            )
        if self.network != self.wallet.network:
            raise ValidationError(
                {
                    "wallet": "The wallet's network should be the same as the network. Network: {} != Wallet network: {}".format(
                        self.network.network, self.wallet.network
                    )
                }
            )
        if self.user_id != self.wallet.user_id:
            raise ValidationError(
                {
                    "user_id": "The wallet must belong to the user who is declared in the owner id. {} != {}".format(
                        self.user_id, self.wallet.user_id
                    )
                }
            )

    class Meta:
        verbose_name = 'Wallet balance'
        verbose_name_plural = 'Wallet balances'
        db_table = 'balance_model'


# <<<=======================================>>> Transaction Models <<<===============================================>>>


class TransactionModel(models.Model, DatetimeFilter, ImageFilter):
    time: int = models.IntegerField(
        verbose_name="The time of creation/sending/acceptance of the transaction",
        validators=[MinValueValidator(10), MaxValueValidator(10)]
    )
    transaction_hash = models.CharField(
        verbose_name="Transaction hash", unique=True, max_length=255,
        null=True, blank=True, default=uuid.uuid4().hex
    )
    fee = models.DecimalField(
        decimal_places=6, max_digits=18, verbose_name="Transaction commission",
        null=True, blank=True, default=0
    )
    amount = models.DecimalField(
        decimal_places=6, max_digits=18, verbose_name="Transaction amount",
        null=True, blank=True, default=0
    )
    inputs = models.JSONField(
        verbose_name="Sender/s transaction", default=dict,
        validators=[TransactionValidators.validate_participants]
    )
    outputs = models.JSONField(
        verbose_name="Recipient/s transaction", default=dict,
        validators=[TransactionValidators.validate_participants]
    )
    status: TransactionStatusModel = models.ForeignKey(
        "TransactionStatusModel", on_delete=models.SET_DEFAULT, default="Unknown",
        db_column="status", verbose_name="Status"
    )
    network: NetworkModel = models.ForeignKey(
        "NetworkModel", on_delete=models.CASCADE, db_column="network",
        verbose_name="Network name", blank=True, null=True
    )
    token: TokenModel = models.ForeignKey(
        "TokenModel", on_delete=models.CASCADE, db_column="token",
        verbose_name="Token name", blank=True, null=True
    )
    user_id: UserModel = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="user_id", verbose_name="Owner id"
    )

    def __str__(self):
        return f"{self.user_id}|{self.network}|{self.transaction_hash[:5]}"

    def save(self, *args, **kwargs):
        if self.network.network == self.token.network:
            super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.token and self.network != self.token.network:
            raise ValidationError(
                {
                    "token": "The token's network must be the same as the network. Network: {} != Token: {}".format(
                        self.network.network, self.token
                    )
                }
            )

    @property
    def correct_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.time)

    @property
    def show_display(self):
        if self.status and self.status.logo.name:
            return UtilsImage.image_url(image_url=self.status.logo.url, method="display")
        else:
            return self.status

    @property
    def show_field(self):
        if self.status and self.status.logo.name:
            return UtilsImage.image_url(image_url=self.status.logo.url, method="field")
        else:
            return self.status


    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        db_table = 'transaction_model'
