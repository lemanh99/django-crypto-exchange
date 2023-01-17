from rest_framework.status import HTTP_200_OK

from crypto.core.common.cryptocurrency_exchange.coinglass import CoinGlassTracking
from crypto.core.utils.dict import get_dict_in_list
from crypto.core.utils.list import sort_list_of_dict


class CoinGlassService:
    def __init__(self):
        self.coin_glass_api = CoinGlassTracking()

    def get_exchange_name_in_list(self, data_funding_rate):
        funding_rate_btc = data_funding_rate[0]
        exchange_name = []
        for margin_list in funding_rate_btc.get('uMarginList'):
            exchange_name.append(margin_list.get("exchangeName"))

        return exchange_name

    def get_funding_rate_exchange_crypto(self):
        status, result = self.coin_glass_api.get_funding_rate()
        if status != HTTP_200_OK:
            return result

        data_funding_rate = result.get('data')
        response_data = {}
        exchanges_name = self.get_exchange_name_in_list(data_funding_rate)
        for funding_rate in data_funding_rate:
            margin_list = funding_rate.get('uMarginList')
            for exchange_name in exchanges_name:

                data = get_dict_in_list(key='exchangeName', value=exchange_name, my_dictlist=margin_list)
                if data.get("status") != 1:
                    continue

                info_funding_rate = dict(
                    symbol=funding_rate.get('symbol'),
                    funding_rate=round(data.get('rate'), 4),
                    funding_rate_detail=data,
                    price=funding_rate.get('uPrice')
                )

                if not response_data.get(exchange_name):
                    response_data[exchange_name] = [info_funding_rate]
                    continue

                response_data.get(exchange_name).append(info_funding_rate)
                response_data[exchange_name] = sort_list_of_dict(response_data[exchange_name],
                                                                 key_sort='funding_rate',
                                                                 reverse=False)

        return response_data

    # Todo fix constant
    def get_funding_rate_big(self, funding_rate_data, min_fr=0.5):
        positive_funding_rate, negative_funding_rate = [], []
        for funding_rate in funding_rate_data:
            rate = funding_rate.get('funding_rate')
            abs_rate = abs(rate)
            if abs_rate > min_fr:
                if rate < 0:
                    negative_funding_rate.append(funding_rate)
                else:
                    positive_funding_rate.append(funding_rate)

        return positive_funding_rate, negative_funding_rate
