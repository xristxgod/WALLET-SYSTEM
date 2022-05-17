from django.db import models

# Create your models here.

class UserModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True, default=False)

class NetworkModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    network = models.CharField(max_length=255, null=False, unique=True)

class TokenModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    network = ""
    token = models.CharField(max_length=255, null=False)
    decimal = models.IntegerField()
    address = models.CharField(max_length=255, null=False)
    token_info = models.JSONField(null=True, blank=True, default={})

class WalletModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    network = ""
    address = models.CharField(max_length=255, null=False)
    private_key = models.CharField(max_length=255, null=False)
    public_key = models.CharField(max_length=255, null=True, blank=True)
    passphrase = models.CharField(max_length=255, null=True, blank=True)
    mnemonic_phrase = models.CharField(max_length=255, null=True, blank=True)
    last_balance = models.DecimalField(default=0)
    user_id = ""

class TransactionStatusModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    status_number = models.IntegerField()
    description = models.TextField(null=True, blank=True)

