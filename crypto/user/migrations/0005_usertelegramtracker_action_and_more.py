# Generated by Django 4.1.3 on 2023-01-07 14:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_usertelegramtracker_expired_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertelegramtracker',
            name='action',
            field=models.CharField(max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usertelegramtracker',
            name='expired_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 10, 14, 46, 11, 603890, tzinfo=datetime.timezone.utc)),
        ),
    ]
