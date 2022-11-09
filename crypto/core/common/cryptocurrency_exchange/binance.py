import logging

import binance.error
from binance.cm_futures import CMFutures
from binance.spot import Spot
from django.conf import settings

logger = logging.getLogger(__name__)


class BinanceFutureApi(CMFutures):
    def mark_price(self, symbol=None):
        """
        | **Mark Price and Funding Rate**

        :API endpoint: ``GET /dapi/v1/premiumIndex``
        :API doc: https://binance-docs.github.io/apidocs/delivery/en/#index-price-and-mark-price

        :parameter symbol: string; the trading pair
        |
        """
        params = {}
        if symbol:
            params.update({
                "symbol": symbol
            })
        return self.query("/dapi/v1/premiumIndex", params)


class BinanceCryptoExchangeFutures:

    def __init__(self):
        api_secret = settings.BINANCE_CRYPTOCURRENCY_EXCHANGE_SECRET
        api_key = settings.BINANCE_CRYPTOCURRENCY_EXCHANGE_KEY
        self.binance_futures_client = BinanceFutureApi(key=api_key, secret=api_secret)

    def get_account_information(self):
        return self.binance_futures_client.account()

    def get_price_coin_in_futures_binance(self, symbol):
        return self.binance_futures_client.mark_price(symbol)


class BinanceCryptoExchangeConnector:

    def __init__(self):
        api_secret = settings.BINANCE_CRYPTOCURRENCY_EXCHANGE_SECRET
        api_key = settings.BINANCE_CRYPTOCURRENCY_EXCHANGE_KEY
        self.client = Spot(key=api_key, secret=api_secret)
