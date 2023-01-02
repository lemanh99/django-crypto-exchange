from django.db import models


# Create your models here.

class CryptoToken(models.Model):
    name = models.CharField(max_length=5)
    address = models.CharField(max_length=255)

    class Meta:
        db_table = 'crypto_token'
        app_label = 'master'


class CryptoExchange(models.Model):
    exchange_id = models.CharField(max_length=5)
    name = models.CharField(max_length=5)
    address = models.CharField(max_length=255)
    exchange = models.CharField(max_length=5)

    class Meta:
        db_table = 'crypto_exchange'
        app_label = 'master'
