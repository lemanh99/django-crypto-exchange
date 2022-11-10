import json
import os
from operator import itemgetter

from crypto.core.common.constants import PoloniexField
from crypto.core.common.cryptocurrency_exchange.poloniex import PoloniexCryptoExchange
from crypto.core.utils.json import save_data_file_json, get_data_file_json


class PoloniexService:
    def __init__(self):
        self.poloniex_exchange = PoloniexCryptoExchange()

    def __get_ticker_market(self, req_data):
        """
         Response return
            Field	Data Type	Description
            symbol	    String	symbol name
            open	    String	price at the start time
            low	        String	lowest price over the last 24h
            high	    String	highest price over the last 24h
            close	    String	price at the end time
            quantity	String	base units traded over the last 24h
            amount	    String	quote units traded over the last 24h
            tradeCount	Integer	count of trades
            startTime	Long	start time for the 24h interval
            closeTime	Long	close time for the 24h interval
            displayName	String	symbol display name
            dailyChange	String	daily change in decimal
            ts	Long	time the record was pushed
        """
        data = self.poloniex_exchange.get_market_ticker(symbol=req_data.get('symbol', None))
        return data

    @staticmethod
    def __get_coin_traded(data):
        return [
            symbol_trade.get(
                PoloniexField.SYMBOL
            ) for symbol_trade in data if symbol_trade.get(PoloniexField.TRADE_COUNT, 0) > 100
        ]

    def __get_structure_triangular_pairs(self, req_data):
        data = self.__get_ticker_market(
            req_data=req_data
        )
        coin_trades = self.__get_coin_traded(
            data=data
        )
        remove_duplicates_list, structure_triangular_pairs_data = [], []
        for pair_a in coin_trades:
            pair_a_split = pair_a.split('_')
            a_base = pair_a_split[0]
            a_quote = pair_a_split[1]
            a_pair_box = [a_base, a_quote]
            for pair_b in coin_trades:
                if pair_a == pair_b:
                    continue

                pair_b_split = pair_b.split('_')
                b_base = pair_b_split[0]
                b_quote = pair_b_split[1]
                if b_base in a_pair_box or b_quote in a_pair_box:
                    for pair_c in coin_trades:
                        if pair_c == pair_a or pair_c == pair_b:
                            continue

                        pair_c_split = pair_c.split('_')
                        c_base = pair_c_split[0]
                        c_quote = pair_c_split[1]
                        unique_item = ''.join(sorted([pair_a, pair_b, pair_c]))
                        if unique_item in remove_duplicates_list:
                            continue

                        pair_box = [a_base, a_quote, b_base, b_quote, c_base, c_quote]
                        if pair_box.count(c_base) == 2 and pair_box.count(c_quote) == 2 and c_base != c_quote:
                            match_dict = {
                                'a_base': a_base,
                                'b_base': c_base,
                                'c_base': c_base,
                                'a_quote': a_quote,
                                'b_quote': b_quote,
                                'c_quote': c_quote,
                                'pair_a': pair_a,
                                'pair_b': pair_b,
                                'pair_c': pair_c,
                                "combined": f'{pair_a},{pair_b},{pair_c}'
                            }
                            remove_duplicates_list.append(unique_item)
                            structure_triangular_pairs_data.append(match_dict)

        return structure_triangular_pairs_data

    def get_pair_trade_arbitrage(self, req_data):
        structure_triangular_pairs_data = self.__get_structure_triangular_pairs(
            req_data=req_data
        )
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_name = f"{dir_path}/assets/structured_triangular_pairs.json"
        save_data_file_json(
            file_name=file_name, data=structure_triangular_pairs_data
        )

        return structure_triangular_pairs_data

    def trade_arbitrage(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_name = f"{dir_path}/assets/structured_triangular_pairs.json"
        structure_triangular_pairs_data = get_data_file_json(file_name)
        return structure_triangular_pairs_data
