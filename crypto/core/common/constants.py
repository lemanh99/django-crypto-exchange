from enum import Enum


class PoloniexField(str, Enum):
    SYMBOL = 'symbol'
    TRADE_COUNT = 'tradeCount'
    BIDS = 'bids'
    ASKS = 'asks'
    SYMBOL_TRADE_LIMIT = 'symbolTradeLimit'
    HIGHEST_BID = 'highestBid'
    LOWEST_ASK = 'lowestAsk'
