from email import message
from operator import itemgetter

import binance.error
from rest_framework import status

from crypto.core.common.cryptocurrency_exchange.binance import BinanceCryptoExchangeFutures


class BinanceService:
    def __init__(self):
        self.binance_futures = BinanceCryptoExchangeFutures()

    def get_account_information(self):
        data = self.binance_futures.get_account_information()
        return data

    def get_funding_rate_binance(self, req_data):
        try:
            symbol = None
            if req_data.get('symbol'):
                symbol = f"{req_data.get('symbol')}USD_PERP"

            data_futures = self.binance_futures.get_price_coin_in_futures_binance(symbol)
            data = [
                dict(
                    symbol=data.get('symbol'),
                    pair=data.get('pair'),
                    price=round(float(data.get('markPrice')), 4),
                    funding_rate=float(data.get('lastFundingRate'))*100,
                    abs_funding_rate=abs(float(data.get('lastFundingRate'))*100),
                    position='LONG' if float(data.get('lastFundingRate')) > 0 else 'SHORT'
                ) for data in data_futures if data.get('lastFundingRate')
            ]
            return status.HTTP_200_OK, sorted(data, key=itemgetter('abs_funding_rate'), reverse=True)
        except binance.error.ClientError as ex:
            return ex.status_code, dict(message=ex.error_message, error_code=ex.error_code)
