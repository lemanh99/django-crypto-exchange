import time
from datetime import datetime, timedelta

import pytz
from django.conf import settings

from crypto.core.common.cryptocurrency_exchange.coingecko import CoinGeckoMarketApi
from crypto.core.common.tracking.blockchair import BlockChairTracking
from crypto.core.utils.dict import get_dict_in_list, get_list_dict_in_list_by_value
from crypto.core.utils.json import get_data_file_json


class BlockchairService:

    @classmethod
    def get_data_analysis_transaction_history(
            cls,
            data_hold,
            transaction_histories,
            price_token,
            time_ago,
            min_order_exchange,
    ):
        holder_address = data_hold.get("address")
        name_holder_address = data_hold.get("name")
        name_exchange = data_hold.get("exchange")
        value_in_exchange, value_out_exchange = 0, 0
        number_in_exchange, number_out_exchange = 0, 0
        value_in_big_order, value_out_big_order = 0, 0
        number_in_big_order, number_out_big_order = 0, 0
        data_analysis = []

        for transaction_history in transaction_histories:
            sender_address = transaction_history.get("sender")
            recipient_address = transaction_history.get("recipient")
            value_usd = round(float(transaction_history.get("value_approximate")) * float(price_token))
            time_transaction = datetime.strptime(
                transaction_history.get("time"), "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=pytz.utc)

            if time_ago and datetime.now(pytz.utc) - timedelta(minutes=int(time_ago)) > time_transaction:
                break

            data_analysis.append(dict(
                status="OUT" if sender_address == holder_address else "IN",
                from_address=name_holder_address if sender_address == holder_address else sender_address,
                to_address=name_holder_address if recipient_address == holder_address else recipient_address,
                quantity=transaction_history.get("value_approximate"),
                age=time.strftime("%H:%M:%S", time.gmtime(
                    (datetime.now(tz=pytz.utc) - time_transaction).total_seconds()
                )),
                value_usd=f'{value_usd} (USD)'
            ))

            if sender_address == holder_address:
                value_out_exchange = value_out_exchange + value_usd
                number_out_exchange = number_out_exchange + 1
                if min_order_exchange and value_usd > float(min_order_exchange):
                    value_out_big_order = value_out_big_order + value_usd
                    number_out_big_order = number_out_big_order + 1
            else:
                value_in_exchange = value_in_exchange + value_usd
                number_in_exchange = number_in_exchange + 1
                if min_order_exchange and value_usd > float(min_order_exchange):
                    value_in_big_order = value_in_big_order + value_usd
                    number_in_big_order = number_in_big_order + 1

        datetime_now = datetime.now(pytz.utc)
        datetime_from = datetime.now(pytz.utc) - timedelta(minutes=int(time_ago)) if time_ago else None
        return dict(
            price_token=price_token,
            name_exchange=name_exchange,
            value_exchange=value_in_exchange + value_out_exchange,
            value_in_exchange=value_in_exchange,
            value_out_exchange=value_out_exchange,
            number_in_exchange=number_in_exchange,
            number_out_exchange=number_out_exchange,
            value_in_big_order=value_in_big_order,
            number_in_big_order=number_in_big_order,
            value_out_big_order=value_out_big_order,
            number_out_big_order=number_out_big_order,
            value_big_order=value_in_big_order + value_out_big_order,
            transaction_history=data_analysis,
            datetime_to=datetime_now.astimezone(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%H:%M:%S %d-%m-%Y"),
            datetime_from=datetime_from.astimezone(pytz.timezone('Asia/Ho_Chi_Minh')).strftime(
                "%H:%M:%S %d-%m-%Y") if datetime_from else None
        )

    def get_history_transaction(self, req_data):
        token_address = req_data.get("token_address")
        holder_address = req_data.get("holder_address")
        file_name = f"{settings.BASE_DIR}/crypto/assets/crypto_exchange_address.json"
        address_exchanges = get_data_file_json(file_name)
        data_hold = get_dict_in_list("address", holder_address, address_exchanges)
        if not data_hold:
            data_hold = dict(
                name=holder_address,
                address=holder_address,
                exchange=holder_address,
            )
        coingecko_api = CoinGeckoMarketApi()
        contract_information = coingecko_api.get_contact_information("ethereum", token_address)
        tickets = contract_information.get("tickers")
        if not tickets:
            return {}

        price = float(tickets[0].get("last"))
        etherscan_tracking = BlockChairTracking()
        status, result = etherscan_tracking.get_history_transaction_holder_erc20_token(
            token_address=token_address,
            holder_address=holder_address
        )
        if result['context'].get('error'):
            return result['context']

        transaction_histories = result["data"].get(holder_address).get("transactions")
        time_ago = req_data.get("time_ago", None)
        min_order_exchange = req_data.get("min_order_exchange", None)
        return self.get_data_analysis_transaction_history(
            data_hold,
            transaction_histories,
            price,
            time_ago,
            min_order_exchange
        )

    def get_analysis_token_by_exchange(self, req_data):
        token_address = req_data.get("token_address")
        exchange_id = req_data.get("exchange_id")
        name_exchange = req_data.get("name_exchange")
        file_name = f"{settings.BASE_DIR}/crypto/assets/crypto_exchange_address.json"
        address_exchanges = get_data_file_json(file_name)

        if exchange_id:
            data_holds = get_list_dict_in_list_by_value("exchange_id", exchange_id, address_exchanges)
        elif name_exchange:
            data_holds = get_list_dict_in_list_by_value("name", name_exchange, address_exchanges)
        else:
            return dict(error="Address exchange empty")

        coingecko_api = CoinGeckoMarketApi()
        contract_information = coingecko_api.get_contact_information("ethereum", token_address)
        tickets = contract_information.get("tickers")
        if not tickets:
            return {}

        price = float(tickets[0].get("last"))

        data_analysis = []
        for data_hold in data_holds:
            holder_address = data_hold.get("address")
            etherscan_tracking = BlockChairTracking()
            status, result = etherscan_tracking.get_history_transaction_holder_erc20_token(
                token_address=token_address,
                holder_address=holder_address
            )
            if result['context'].get('error'):
                return result['context']

            transaction_histories = result["data"].get(holder_address).get("transactions")
            time_ago = req_data.get("time_ago", None)
            min_order_exchange = req_data.get("min_order_exchange", None)
            data = self.get_data_analysis_transaction_history(
                data_hold,
                transaction_histories,
                price,
                time_ago,
                min_order_exchange
            )
            data_analysis.append(data)
        return data_analysis
