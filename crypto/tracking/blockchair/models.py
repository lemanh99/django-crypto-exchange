from django.db import models


class BlockchairRequest(models.Model):
    user_login = models.CharField(max_length=255)
    total = models.IntegerField(default=100000)
    number_request = models.IntegerField()

    class Meta:
        db_table = 'blockchair_request'
        app_label = 'blockchair'
