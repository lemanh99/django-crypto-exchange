from django.conf import settings

from crypto import settings
from crypto.poloniex.polo_sdk_python.polosdk import RestClient as PoloniexRestClient


class PoloniexCryptoExchange:
    def __init__(self):
        self.access_key = settings.POLONIEX_CRYPTOCURRENCY_EXCHANGE_KEY
        self.secret_key = settings.POLONIEX_CRYPTOCURRENCY_EXCHANGE_SECRET
        self.poloniex_client = PoloniexRestClient(
            api_key=self.access_key,
            api_secret=self.secret_key
        )

    def get_markets(self, symbol):
        if not symbol:
            return self.poloniex_client.get_markets()

        return self.poloniex_client.get_market(symbol)

    def get_market_ticker(self, symbol):
        if not symbol:
            return self.poloniex_client.markets.get_ticker24h_all()

        return self.poloniex_client.markets.get_ticker24h(symbol)

    def get_market_price(self, symbol):
        if not symbol:
            return self.poloniex_client.markets.get_prices()

        return self.poloniex_client.markets.get_price(symbol)

    def get_market_order_book(self, symbol):
        return self.poloniex_client.markets.get_orderbook(symbol)
