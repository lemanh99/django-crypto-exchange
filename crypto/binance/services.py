from operator import itemgetter

from crypto.core.common.cryptocurrency_exchange.binance import BinanceCryptoExchangeFutures


class BinanceService:
    def __init__(self):
        self.binance_futures = BinanceCryptoExchangeFutures()

    def get_account_information(self):
        data = self.binance_futures.get_account_information()
        return data

    def get_funding_rate_binance(self):
        data_futures = self.binance_futures.get_price_coin_in_futures_binance()
        data = [
            dict(
                symbol=data.get('symbol'),
                pair=data.get('pair'),
                funding_rate=float(data.get('lastFundingRate')),
                abs_funding_rate=abs(float(data.get('lastFundingRate')))
            ) for data in data_futures if data.get('lastFundingRate')
        ]
        return sorted(data, key=itemgetter('abs_funding_rate'), reverse=True)
