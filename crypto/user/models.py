from datetime import datetime, timezone, timedelta

from django.db import models


# Create your models here.

class UserTelegramTracker(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    username = models.CharField(max_length=15, null=True, blank=True)
    step_current = models.IntegerField()
    commands = models.CharField(max_length=255)
    text_input = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_telegram_tracker'
        app_label = 'user'
