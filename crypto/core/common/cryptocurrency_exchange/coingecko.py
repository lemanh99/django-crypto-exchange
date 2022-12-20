from pycoingecko import CoinGeckoAPI


class CoinGeckoMarketApi(CoinGeckoAPI):
    def __init__(self):
        super().__init__()

    def get_tickets(self, symbol, params: dict = {}):
        filter_params = {
            'exchange_ids': params.get('exchange_ids')
        }
        return self.get_coin_ticker_by_id(symbol, **filter_params)
