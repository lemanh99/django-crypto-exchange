from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone


# Create your models here.

class UserTelegramTracker(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    username = models.CharField(max_length=15, null=True, blank=True)
    uuid = models.CharField(max_length=50)
    token_tracker = models.CharField(max_length=255)
    expired_date = models.DateTimeField(default=datetime.now(tz=timezone.utc) + timedelta(days=3))

    class Meta:
        db_table = 'user_telegram_tracker'
        app_label = 'user'
