# Generated by Django 4.1.3 on 2023-01-08 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_usertelegramtracker_action_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertelegramtracker',
            name='expired_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
