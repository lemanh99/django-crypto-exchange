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
    UNKNOWN_COMMAND = "OOps...We didn't recognise the command: {text}"
