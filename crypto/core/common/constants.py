from enum import Enum


class PoloniexField(str, Enum):
    SYMBOL = 'symbol'
    TRADE_COUNT = 'tradeCount'
    BIDS = 'bids'
    ASKS = 'asks'
    SYMBOL_TRADE_LIMIT = 'symbolTradeLimit'
    HIGHEST_BID = 'highestBid'
    LOWEST_ASK = 'lowestAsk'


class StableCoin(str, Enum):
    USDD = 'usdd'
    DAI = 'dai'
    USDT = 'usdt'
    USDC = 'usdc'
    TUSD = 'tusd'
    BUSD = 'busd'
