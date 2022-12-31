from pycoingecko import CoinGeckoAPI


class CoinGeckoMarketApi(CoinGeckoAPI):
    def __init__(self):
        super().__init__()

    def get_tickets(self, symbol, params: dict = {}):
        filter_params = {
            'exchange_ids': params.get('exchange_ids')
        }
        print(symbol)
        return self.get_coin_ticker_by_id(symbol, **filter_params)

    def get_coin_markets(self, params: dict = {}):
        vs_currency = params.get('vs_currency', 'usd')
        filter_params = {
            'ids': params.get('symbol'),
            'category': params.get('category', 'arbitrum-ecosystem'),
            'per_page': params.get('per_page', 300),
            'page': params.get('page', 1),
        }
        return self.get_coins_markets(vs_currency, **filter_params)

    def get_exchange_ticket(self, exchange_id, params: dict = {}):
        filter_params = {
            'page': params.get('page', 1),
            # 'order': params.get('volume_asc', ""),
        }
        return self.get_exchanges_tickers_by_id(exchange_id, **filter_params)

    def get_contact_information(self, platform, contract_address):
        return self.get_coin_info_from_contract_address_by_id(platform, contract_address)
