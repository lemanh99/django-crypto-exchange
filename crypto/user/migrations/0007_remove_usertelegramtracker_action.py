# Generated by Django 4.1.3 on 2023-01-08 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_usertelegramtracker_expired_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertelegramtracker',
            name='action',
        ),
    ]