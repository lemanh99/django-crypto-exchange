import logging

from django.core.management.base import BaseCommand
from django.utils import autoreload

from crypto.social.telegram_bot.server import run_telegram_bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'port',
            nargs='?',
            type=int,
        )

    def handle(self, *args, **options):
        port = options.get('port', None)
        if port:
            autoreload.run_with_reloader(run_telegram_bot, args=None, kwargs=None)
        else:
            run_telegram_bot()
