from django.db import models

from api.utils.types import CoinsHelper

class UserModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True, default=False)

    def save(self, *args, **kwargs):
        if self.username.find("@") == -1:
            self.username = f"@{self.username}"
        super(self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'user_model'

class NetworkModel(models.Model):
    network = models.CharField(primary_key=True, max_length=255, null=False, unique=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.network = self.network.upper()
        super(self).save(*args, **kwargs)

    def __str__(self):
        return self.network

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Networks'
        db_table = 'network_model'

class TokenModel(models.Model):
    token = models.CharField(primary_key=True, max_length=255, null=False)
    network: NetworkModel = models.ForeignKey('NetworkModel', on_delete=models.CASCADE, db_column="network")
    decimals = models.IntegerField()
    address = models.CharField(max_length=255, null=False, unique=True)
    token_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.network.network}-{self.token}"

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        db_table = 'token_model'

class WalletModel(models.Model):
    address = models.CharField(max_length=255, null=False, unique=True)
    private_key = models.CharField(max_length=255, null=False, unique=True)
    public_key = models.CharField(max_length=255, null=True, blank=True, unique=True)
    passphrase = models.CharField(max_length=255, null=True, blank=True)
    mnemonic_phrase = models.CharField(max_length=255, null=True, blank=True, unique=True)
    network: NetworkModel = models.ForeignKey('NetworkModel', on_delete=models.CASCADE, db_column="network")
    user_id: UserModel = models.ForeignKey('UserModel', on_delete=models.CASCADE, db_column="user_id")

    def __str__(self):
        return f"{self.network.network} | {self.user_id.username}"

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        db_table = 'wallet_model'

class TransactionStatusModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Transaction status'
        verbose_name_plural = 'Transaction statuses'
        db_table = 'transaction_status_model'

class TransactionModel(models.Model):
    time = models.IntegerField()
    transaction_hash = models.CharField(max_length=255, unique=True, default="-")
    fee = models.DecimalField(default=0, decimal_places=6, max_digits=18)
    amount = models.DecimalField(default=0, decimal_places=6, max_digits=18)
    inputs = models.JSONField(null=True, blank=True)
    outputs = models.JSONField(null=True, blank=True)
    network: NetworkModel = models.ForeignKey('NetworkModel', on_delete=models.CASCADE, db_column="network")
    token: TokenModel = models.ForeignKey(
        'TokenModel', on_delete=models.CASCADE,
        db_column="token", null=True, blank=True
    )
    status: TransactionStatusModel = models.ForeignKey(
        'TransactionStatusModel', on_delete=models.CASCADE, db_column="status"
    )
    user_id: UserModel = models.ForeignKey('UserModel', on_delete=models.CASCADE, db_column="user_id")

    def save(self, *args, **kwargs):
        if self.token is not None and (self.token.network == self.network.network):
            super(self).save(*args, **kwargs)

    def __str__(self):
        token = self.token.token if self.token is not None else CoinsHelper.get_native_by_network(
            network=self.network.network
        )
        return f"{self.network.network}-{token} | {self.user_id.username}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        db_table = 'transaction_model'

class BalanceModel(models.Model):
    balance = models.DecimalField(default=0, decimal_places=6, max_digits=18)
    wallet: WalletModel = models.ForeignKey(
        'WalletModel', on_delete=models.CASCADE, db_column="wallet"
    )
    token: TokenModel = models.ForeignKey(
        'TokenModel', on_delete=models.CASCADE, db_column="token", null=True, blank=True
    )
    network: NetworkModel = models.ForeignKey(
        'NetworkModel', on_delete=models.CASCADE, db_column="network"
    )
    user_id: UserModel = models.ForeignKey(
        'UserModel', on_delete=models.CASCADE, db_column="user_id"
    )

    def save(self, *args, **kwargs):
        if self.token is not None and (self.network.network == self.token.token) and \
                (self.user_id.id == self.wallet.user_id.id):
            super(self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_id.username} | {self.network.network}-{self.token.token}"

    class Meta:
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'
        db_table = 'balance_model'