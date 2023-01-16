from datetime import datetime

import pytz
from django.template import Context
from django.template.loader import get_template
from rest_framework.status import HTTP_200_OK

from crypto.core.common.cryptocurrency_exchange.coinglass import CoinGlassTracking
from crypto.core.utils.dict import get_dict_in_list
from crypto.core.utils.list import sort_list_of_dict


class CoinGlassService:
    def __init__(self):
        self.coin_glass_api = CoinGlassTracking()

    def get_funding_rate_exchange_crypto(self, exchange_name='Binance'):
        status, result = self.coin_glass_api.get_funding_rate()
        if status != HTTP_200_OK:
            return result

        data_funding_rate = result.get('data')
        response_data = []
        for funding_rate in data_funding_rate:
            margin_list = funding_rate.get('uMarginList')
            data = get_dict_in_list(key='exchangeName', value=exchange_name, my_dictlist=margin_list)
            if data.get("status") != 1:
                continue

            response_data.append(dict(
                symbol=funding_rate.get('symbol'),
                funding_rate=data.get('rate'),
                funding_rate_detail=data,

            ))
        return sort_list_of_dict(response_data, key_sort='funding_rate', reverse=False)

    def get_funding_rate_big(self, min_fr=0.12):
        funding_rate_data = self.get_funding_rate_exchange_crypto()
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

    def get_template_fr(self):
        template = get_template("telegram/notification_funding_rate.html")
        positive_funding_rate, negative_funding_rate = self.get_funding_rate_big()

        data = {
            'datetime_now': datetime.now(pytz.utc).astimezone(pytz.timezone(
                'Asia/Ho_Chi_Minh')
            ).strftime("%H:%M:%S %d-%m-%Y"),
            'funding_rate_type': 'POSITIVE',
            'command_future': 'SHORT',
            'funding_rate_data': positive_funding_rate
        }
        render_context = Context(dict(**data))
        html = template.template.render(render_context)
        return 200
