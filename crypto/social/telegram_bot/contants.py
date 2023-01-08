from enum import Enum


class CommandsEnum(str, Enum):
    START = 'start'
    HELP = 'Help'
    MORE_OPTIONS = "More Options"
    BACK_BUTTON_PRETEXT = "Back TO << "
    CANCEL = 'Cancel'
    TOKEN = "Token"
    ADDRESS = "Address"
    EXCHANGE = "Exchange"
    TYPE_TOKEN_CRYPTO = "Type Token Exchange"
    SYMBOL_BINANCE = "symbol_binance"
    CRYPTO_EXCHANGE = "Crypto Exchange"
    ANALYSIS_CRYPTO_DATA = "analysis crypto data"
    TIME_EXCHANGE = "Time exchange"
    ALL = "All"


class MenuTelegram(Enum):
    REPLY_KEYBOARDS = {
        'default': [
            [CommandsEnum.TOKEN, CommandsEnum.EXCHANGE, CommandsEnum.ADDRESS],
            [CommandsEnum.HELP, CommandsEnum.CANCEL, CommandsEnum.MORE_OPTIONS],
        ]
    }


class Position(str, Enum):
    TOP = 't'
    BOTTOM = 'b'


class Message(str, Enum):
    WELCOME_TEXT = "Hi. Welcome to the bot Le Manh"
    HELP_TEXT = "How can i help you."
    SELECT_OPTION = "Please select option: "
    SELECT_TOKEN = "please select token"
    ENTER_ADDRESS = "please enter address contract ethereum"
    EXCHANGE = "please select exchange crypto: "
    SELECT_CRYPTO_EXCHANGE = "please select crypto exchange"
    SELECT_TIME_EXCHANGE = "please select crypto exchange time"
    UNKNOWN_COMMAND = "OOps...We didn't recognise the command: {text}"
    UNKNOWN_ERROR = "Sorry...An unknown error has occurred"
    GOODBYE = "Goodbye!!"


class TimeExchange(Enum):
    FIVE_MINUTES = 5, "5 minutes"
    THIRTY_MINUTES = 30, "30 minutes"
    ONE_HOUR = 60, "1 hours"
    THREE_HOUR = 3 * 60, "3 hours"
    SIX_HOUR = 6 * 60, "6 hours"
    TWELVE_HOUR = 12 * 60, "12 hours"
    TWENTY_FOUR_HOUR = 24 * 60, "24 hours"

    @property
    def minutes(self):
        return self.value[0]

    @property
    def name(self):
        return self.value[1]


class CryptoExchange(str, Enum):
    BINANCE = 'binance'


class BaseCryptoEnum(Enum):
    @property
    def name(self):
        return self.value[0]

    @property
    def variable(self):
        return self.value[1]


class TypeCryptoExchange(BaseCryptoEnum):
    SPOT = 'Token spot', 'spot'
    FUTURES = 'Token futures', 'futures'
    INPUT_SYMBOL = 'Input symbol', 'InputSymbol'


class StepBot(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
