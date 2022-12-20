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
