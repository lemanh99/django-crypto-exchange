from crypto.social.telegram_bot.echobot.echobot_v1 import run_telegram_bot_v1
from crypto.social.telegram_bot.echobot.echobot_v2 import run_telegram_bot_v2


def run_telegram_bot(version=1):
    run_version = {
        1: lambda: run_telegram_bot_v1(),
        2: lambda: run_telegram_bot_v2(),
    }
    run_version.get(version)()


if __name__ == '__main__':
    run_telegram_bot()
