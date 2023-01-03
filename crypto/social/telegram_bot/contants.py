from enum import Enum


class CommandsEnum(str, Enum):
    START = 'Start'
    HELP = 'Help'
    MORE_OPTIONS = "More Options"
    BACK_BUTTON_PRETEXT = "Back TO << "
    CANCEL = 'Cancel'
    TOKEN = "Token"
    CRYPTO_EXCHANGE = "Crypto Exchange"
    ANALYSIS_CRYPTO_DATA = "analysis crypto data"
    TIME_EXCHANGE = "Time exchange"
    ALL = "All"


class MenuTelegram(Enum):
    REPLY_KEYBOARDS = {
        'default': [
            [CommandsEnum.TOKEN],
            [CommandsEnum.HELP, CommandsEnum.MORE_OPTIONS],
            [CommandsEnum.CANCEL]
        ]
    }


class Position(str, Enum):
    TOP = 't'
    BOTTOM = 'b'


class Message(str, Enum):
    WELCOME_TEXT = "Hi. Welcome to the bot Le Manh"
    HELP_TEXT = "How can i help you."
    SELECT_TOKEN = "please select token"
    SELECT_CRYPTO_EXCHANGE = "please select crypto exchange"
    SELECT_TIME_EXCHANGE = "please select crypto exchange time"
    UNKNOWN_COMMAND = "OOps...We didn't recognise the command: {text}"
    GOODBYE = "Goodbye!!"


class TimeExchange(Enum):
    FIVE_MINUTES = 5, "5 minutes"
    THIRTY_MINUTES = 30, "30 minutes"
    ONE_HOUR = 60, "1 hours"
    TWELVE_HOUR = 12 * 60, "12 hours"
    TWENTY_FOUR_HOUR = 24 * 60, "24 hours"

    @property
    def minutes(self):
        return self.value[0]

    @property
    def name(self):
        return self.value[1]
