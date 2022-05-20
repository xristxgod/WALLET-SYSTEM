from django.db import models

class UserModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'user_model'

class NetworkModel(models.Model):
    network = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.network

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Networks'
        db_table = 'network_model'

class TokenModel(models.Model):
    network: NetworkModel = models.ForeignKey('NetworkModel', on_delete=models.CASCADE, db_column="network")
    token = models.CharField(max_length=255, null=False)
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
    network: NetworkModel = models.ForeignKey('NetworkModel', on_delete=models.CASCADE, db_column="network")
    address = models.CharField(max_length=255, null=False, unique=True)
    private_key = models.CharField(max_length=255, null=False, unique=True)
    public_key = models.CharField(max_length=255, null=True, blank=True, unique=True)
    passphrase = models.CharField(max_length=255, null=True, blank=True)
    mnemonic_phrase = models.CharField(max_length=255, null=True, blank=True, unique=True)
    last_balance = models.DecimalField(default=0, max_digits=10, decimal_places=10)
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
    status_number = models.IntegerField(unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Transaction status'
        verbose_name_plural = 'Transaction statuses'
        db_table = 'transaction_status_model'

class TransactionModel(models.Model):
    network: NetworkModel = models.ForeignKey('NetworkModel', on_delete=models.CASCADE, db_column="network")
    time = models.IntegerField()
    transaction_hash = models.CharField(max_length=255, unique=True)
    fee = models.DecimalField(default=0, max_digits=10, decimal_places=10)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=10)
    senders = models.JSONField(null=True, blank=True)
    recipients = models.JSONField(null=True, blank=True)
    token: TokenModel = models.ForeignKey('TokenModel', on_delete=models.CASCADE, db_column="token")
    status: TransactionStatusModel = models.ForeignKey(
        'TransactionStatusModel', on_delete=models.CASCADE, db_column="status"
    )
    user_id: UserModel = models.ForeignKey('UserModel', on_delete=models.CASCADE, db_column="user_id")

    def __str__(self):
        return f"{self.network.network}-{self.token.token} | {self.user_id.username}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        db_table = 'transaction_model'