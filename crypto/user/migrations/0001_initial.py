# Generated by Django 4.1.3 on 2023-01-06 08:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserTelegramTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=15, null=True)),
                ('username', models.CharField(blank=True, max_length=15, null=True)),
                ('uuid', models.CharField(max_length=50)),
                ('token_tracker', models.CharField(max_length=255)),
                ('expired_date', models.DateTimeField(default=datetime.datetime(2023, 1, 9, 8, 25, 9, 300024, tzinfo=datetime.timezone.utc))),
            ],
            options={
                'db_table': 'user_telegram_tracker',
            },
        ),
    ]
