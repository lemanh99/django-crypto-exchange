import logging

from django.core.management.base import BaseCommand

from crypto.social.telegram_bot.echobot import run_telegram_bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        run_telegram_bot()
