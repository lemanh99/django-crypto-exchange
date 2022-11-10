from enum import Enum


class PoloniexField(str, Enum):
    SYMBOL = 'symbol'
    TRADE_COUNT = 'tradeCount'
