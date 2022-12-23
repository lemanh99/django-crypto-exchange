import decimal
import time
from datetime import datetime
from operator import itemgetter

import babel.numbers

from crypto.core.common.constants import StableCoin
from crypto.core.common.cryptocurrency_exchange.coingecko import CoinGeckoMarketApi


class CoinGeckoService:
    def __init__(self):
        self.cg_market = CoinGeckoMarketApi()

    def get_percent_market_exchange(self, req_data):
        symbol = req_data.get('symbol')
        tickets_data = self.cg_market.get_tickets(
            symbol=symbol,
            params=req_data
        )
        market_data = self.get_market_data_coins(tickets_data.get("tickers"), symbol=symbol)
        return market_data

    def get_market_data_coins(self, tickets_data, symbol):
        market_data = []
        for ticket_data in tickets_data:
            if '0X' not in ticket_data.get("base"):
                pair = f'{ticket_data.get("base")}/{ticket_data.get("target")}'
            else:
                pair = f'{symbol}/{ticket_data.get("target_coin_id")}'

            market_data.append(dict(
                pair=pair,
                name_market=ticket_data['market'].get('name'),
                price_last=ticket_data.get("last"),
                spread=f'{round(ticket_data.get("bid_ask_spread_percentage"), 5)}%'
            ))

        return market_data

    def get_coin_exchange_market(self, blockchain_ecosystem, req_data):
        req_data._mutable = True
        req_data['category'] = blockchain_ecosystem
        coins_markets = self.cg_market.get_coin_markets(req_data)
        data = self.get_information_coin_markets(coins_markets, req_data)
        return data

    def get_coin_exchange_dex(self, exchange_id, req_data):
        req_data._mutable = True
        number_pages = req_data['number_pages']
        information_coins = []
        for number_page in range(1, number_pages + 1):
            req_data['page'] = number_page
            coins_markets = self.cg_market.get_exchange_ticket(exchange_id, req_data)
            data = self.get_information_coin_markets(coins_markets.get('tickers'), req_data)
            information_coins.extend(data)
        return information_coins

    def get_information_coin_markets(self, coins_markets, req_data):
        data = []
        stable_coin = [coin.value for coin in StableCoin]
        max_market_cap = req_data.get('max_market_cap', None)
        for index, coin_market in enumerate(coins_markets):
            if coin_market.get('symbol') in stable_coin:
                continue

            if max_market_cap and coin_market.get('market_cap') and int(coin_market.get('market_cap', "0")) > int(
                    max_market_cap):
                continue

            params = {
                'exchange_ids': req_data.get('exchange_ids')
            }
            time.sleep(0.5)
            tickets_data = self.cg_market.get_tickets(
                symbol=coin_market.get('id') or coin_market.get("coin_id"),
                params=params
            )
            exchange_data = []
            exchange_data_merge = []
            for ticket in tickets_data['tickers']:
                if ticket.get("target", '').lower() not in stable_coin:
                    continue

                volume = float(ticket.get('volume'))

                ticket_information = dict(
                    pair=f'{ticket.get("base")}/{ticket.get("target")}',
                    market_name=ticket['market'].get('name'),
                    spread=f'{round(ticket.get("bid_ask_spread_percentage"), 5)}%',
                    trust_score=ticket['trust_score'],
                    price_last=ticket['last'],
                    price_high=float(ticket['last']) + float(ticket['last']) * round(
                        float(ticket.get("bid_ask_spread_percentage")), 5
                    ) / 100,
                    last_trade=datetime.fromisoformat(ticket['last_traded_at']).strftime("%m/%d/%Y %H:%M:%S")
                )
                ticket_information_join = f"{ticket_information.get('price_last')}  -  {ticket_information.get('price_high')}   -  " \
                                          f"{ticket_information.get('market_name')}    -    {ticket_information.get('pair')}  -   " \
                                          f"{ticket_information.get('spread')}  -   {ticket_information.get('last_trade')}-" \
                                          f"{ticket_information.get('trust_score')}"
                exchange_data.append(ticket_information)
                exchange_data_merge.append(ticket_information_join)

            if len(exchange_data) < 2:
                continue

            data.append(dict(
                id=coin_market.get('id'),
                symbol=coin_market.get('symbol'),
                name=coin_market.get('name'),
                # market_cap=babel.numbers.format_currency(decimal.Decimal(coin_market.get('market_cap', "0")), "USD"),
                market_cap_rank=coin_market.get('market_cap_rank', "0"),
                exchange_data_merge=exchange_data_merge,
                exchange_data=exchange_data,
            ))
        return data

    def get_same_coin(self, req_data):
        req_data._mutable = True
        req_data._mutable = True
        number_pages = 10
        mexc_coins = {}
        gate_coins = {}
        for number_page in range(2, number_pages + 1):
            print(number_page)
            req_data['page'] = number_page
            mexc_coins_markets = self.cg_market.get_exchange_ticket('mxc', req_data)
            gate_coins_markets = self.cg_market.get_exchange_ticket('gate', req_data)
            mexc_tickers = mexc_coins_markets.get('tickers')
            gate_tickers = gate_coins_markets.get('tickers')
            for mexc_ticker in mexc_tickers:
                mexc_coins.update({
                    f'{mexc_ticker.get("base")}/{mexc_ticker.get("target")}': dict(
                        spread=f'{round(mexc_ticker.get("bid_ask_spread_percentage"), 5)}%',
                        price_last=mexc_ticker['last'],
                        price_high=float(mexc_ticker['last']) + float(mexc_ticker['last']) * round(
                            float(mexc_ticker.get("bid_ask_spread_percentage")), 5
                        ))
                })

            for gate_ticker in gate_tickers:
                gate_coins.update({
                    f'{gate_ticker.get("base")}/{gate_ticker.get("target")}': dict(
                        spread=f'{round(gate_ticker.get("bid_ask_spread_percentage"), 5)}%',
                        price_last=gate_ticker['last'],
                        price_high=float(gate_ticker['last']) + float(gate_ticker['last']) * round(
                            float(gate_ticker.get("bid_ask_spread_percentage")), 5
                        ))
                })

        information_coins = []
        for pair in list(set(mexc_coins).intersection(gate_coins)):
            round_price = round(mexc_coins[pair].get('price_last'))
            division_factor = 10 ** (len(str(round_price))) if round_price > 0 else 1
            information_coins.append({
                "price_last": abs(
                    float(mexc_coins[pair].get('price_last')) - float(
                        gate_coins[pair].get('price_last'))) / division_factor,
                "cal": abs(
                    float(mexc_coins[pair].get('price_last')) - float(gate_coins[pair].get('price_last'))
                ) * 40 / division_factor,
                pair: {
                    "price_last": float(mexc_coins[pair].get('price_last')) - float(gate_coins[pair].get('price_last')),
                    "price_last_high": float(mexc_coins[pair].get('price_high')) - float(
                        gate_coins[pair].get('price_high')
                    ),
                    "detail": [dict(mexc=mexc_coins.get(pair)), dict(gate=gate_coins.get(pair))],

                },
            })
        return sorted(information_coins, key=itemgetter('price_last'), reverse=True)
