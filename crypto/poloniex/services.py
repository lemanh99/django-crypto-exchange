import json
import os
from operator import itemgetter

from crypto.core.common.constants import PoloniexField
from crypto.core.common.cryptocurrency_exchange.poloniex import PoloniexCryptoExchange
from crypto.core.utils.dict import get_dict_in_list
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

    def __get_markets(self, req_data):
        data = self.poloniex_exchange.get_markets(symbol=req_data.get('symbol', None))
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
                                'b_base': b_base,
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

    def get_lowest_ask_and_highest_bird(self, symbol: str, coin_markets: dict):
        pair_order = coin_markets.get(symbol)
        if not pair_order:
            pair_order = self.poloniex_exchange.get_market_order_book(symbol)
            coin_markets.update({
                symbol: pair_order
            })

        lowest_ask = pair_order.get(PoloniexField.ASKS)[0]
        highest_bird = pair_order.get(PoloniexField.BIDS)[0]
        return lowest_ask, highest_bird

    def __get_price_of_t_pair(self, t_pair: dict, coin_markets: dict):
        pair_a = t_pair['pair_a']
        pair_b = t_pair['pair_b']
        pair_c = t_pair['pair_c']
        pair_a_ask, pair_a_bid = self.get_lowest_ask_and_highest_bird(
            symbol=pair_a,
            coin_markets=coin_markets
        )
        pair_b_ask, pair_b_bid = self.get_lowest_ask_and_highest_bird(
            symbol=pair_b,
            coin_markets=coin_markets
        )
        pair_c_ask, pair_c_bid = self.get_lowest_ask_and_highest_bird(
            symbol=pair_c,
            coin_markets=coin_markets
        )
        return {
            "pair_a_ask": float(pair_a_ask),
            "pair_a_bid": float(pair_a_bid),
            "pair_b_ask": float(pair_b_ask),
            "pair_b_bid": float(pair_b_bid),
            "pair_c_ask": float(pair_c_ask),
            "pair_c_bid": float(pair_c_bid),
        }

    def __cal_triangular_arb_surface_rate(self, t_pair, price_coin):
        starting_amount = 1
        min_surface_rate = 0
        surface_dict = {}
        contract_2 = ""
        contract_3 = ""
        direction_trade_1 = ""
        direction_trade_2 = ""
        direction_trade_3 = ""
        acquired_coin_t2 = 0
        acquired_coin_t3 = 0
        calculated = 0
        pair_a = t_pair["pair_a"]
        pair_b = t_pair["pair_b"]
        pair_c = t_pair["pair_c"]
        a_base = t_pair["a_base"]
        a_quote = t_pair["a_quote"]
        b_base = t_pair["b_base"]
        b_quote = t_pair["b_quote"]
        c_base = t_pair["c_base"]
        c_quote = t_pair["c_quote"]

        a_ask = price_coin["pair_a_ask"]
        a_bid = price_coin["pair_a_bid"]
        b_ask = price_coin["pair_b_ask"]
        b_bid = price_coin["pair_b_bid"]
        c_ask = price_coin["pair_c_ask"]
        c_bid = price_coin["pair_c_bid"]

        direction_list = ["forward", "reverse"]
        for direction in direction_list:
            """
                If we swapping the coin on the left (Base) to the right (Quote) then * (1/ask)
                If we swapping the coin on the right (Quote) to the left (Base) then * bid
            """

            swap_1 = 0
            swap_2 = 0
            swap_3 = 0
            swap_1_rate = 0
            swap_2_rate = 0
            swap_3_rate = 0

            # Assume starting with a_base and swapping for a_quote
            if direction == "forward":
                swap_1 = a_base
                swap_2 = a_quote
                swap_1_rate = 1 / a_ask
                direction_trade_1 = "base_to_quote"

            if direction == "reverse":
                swap_1 = a_quote
                swap_2 = a_base
                swap_1_rate = a_bid
                direction_trade_1 = "base_to_quote"

            # Place first trade
            contract_1 = pair_a
            acquired_coin_t1 = starting_amount * swap_1_rate

            """
            Check if a_quote (acquired_coin) matches b_quote
            """
            if direction == "forward":
                if a_quote == b_quote and calculated == 0:
                    swap_2_rate = b_bid
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "quote_to_base"
                    contract_2 = pair_b

                    # If b_base matches c_base
                    if b_base == c_base:
                        swap_3 = c_base
                        swap_3_rate = 1 / c_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_c

                    if b_base == c_quote:
                        swap_3 = c_quote
                        swap_3_rate = c_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_c

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

            """
            Check if a_quote (acquired_coin) matches b_base
            """
            if direction == "forward":
                if a_quote == b_base and calculated == 0:
                    swap_2_rate = 1 / b_ask
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "base_to_quote"
                    contract_2 = pair_b

                    if b_quote == c_base:
                        swap_3 = c_base
                        swap_3_rate = 1 / c_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_c

                    if b_quote == c_quote:
                        swap_3 = c_quote
                        swap_3_rate = c_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_c

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

            """
            Check if a_quote (acquired_coin) matches c_quote
            """
            if direction == "forward":
                if a_quote == c_quote and calculated == 0:
                    swap_2_rate = c_bid
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "quote_to_base"
                    contract_2 = pair_c

                    # If c_base matches b_base
                    if c_base == b_base:
                        swap_3 = b_base
                        swap_3_rate = 1 / b_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_b

                    if c_base == b_quote:
                        swap_3 = b_quote
                        swap_3_rate = b_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_b

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

            """
            Check if a_quote (acquired_coin) matches c_base
            """
            if direction == "forward":
                if a_quote == c_base and calculated == 0:
                    swap_2_rate = 1 / c_ask
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "base_to_quote"
                    contract_2 = pair_c

                    if c_quote == b_base:
                        swap_3 = b_base
                        swap_3_rate = 1 / b_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_b

                    if c_quote == b_quote:
                        swap_3 = b_quote
                        swap_3_rate = b_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_b

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1
            if direction == "reverse":
                if a_base == b_quote and calculated == 0:
                    swap_2_rate = b_bid
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "quote_to_base"
                    contract_2 = pair_b

                    # If b_base matches c_base
                    if b_base == c_base:
                        swap_3 = c_base
                        swap_3_rate = 1 / c_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_c

                    if b_base == c_quote:
                        swap_3 = c_quote
                        swap_3_rate = c_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_c

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

            """
            Check if a_base (acquired_coin) matches b_base
            """
            if direction == "reverse":
                if a_base == b_base and calculated == 0:
                    swap_2_rate = 1 / b_ask
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "base_to_quote"
                    contract_2 = pair_b

                    if b_quote == c_base:
                        swap_3 = c_base
                        swap_3_rate = 1 / c_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_c

                    if b_quote == c_quote:
                        swap_3 = c_quote
                        swap_3_rate = c_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_c

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

            """
            Check if a_base (acquired_coin) matches c_quote
            """
            if direction == "reverse":
                if a_base == c_quote and calculated == 0:
                    swap_2_rate = c_bid
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "quote_to_base"
                    contract_2 = pair_c

                    # If c_base matches b_base
                    if c_base == b_base:
                        swap_3 = b_base
                        swap_3_rate = 1 / b_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_b

                    if c_base == b_quote:
                        swap_3 = b_quote
                        swap_3_rate = b_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_b

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

            """
            Check if a_quote (acquired_coin) matches c_base
            """
            if direction == "reverse":
                if a_base == c_base and calculated == 0:
                    swap_2_rate = 1 / c_ask
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "base_to_quote"
                    contract_2 = pair_c

                    if c_quote == b_base:
                        swap_3 = b_base
                        swap_3_rate = 1 / b_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_b

                    if c_quote == b_quote:
                        swap_3 = b_quote
                        swap_3_rate = b_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_b

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1
            # Profit loss output
            profit_loss = acquired_coin_t3 - starting_amount
            profit_loss_perc = profit_loss / starting_amount * 100 if profit_loss else 0

            trade_description_1 = f"start with {swap_1} of {starting_amount}. " \
                                  f"Swap at {swap_1_rate} for {swap_2} acquiring {acquired_coin_t1}"
            trade_description_2 = f"Swap at {acquired_coin_t1} for {swap_2} at {swap_2_rate} acquiring {acquired_coin_t2}"
            trade_description_3 = f"Swap at {acquired_coin_t2} for {swap_3} at {swap_2_rate} acquiring {acquired_coin_t3}"

            if profit_loss_perc > min_surface_rate:
                surface_dict = {
                    "swap1": swap_1,
                    "swap_2": swap_2,
                    "swap_3": swap_3,
                    "contract_1": contract_1,
                    "contract_2": contract_2,
                    "contract_3": contract_3,
                    "direction_trade_1": direction_trade_1,
                    "direction_trade_2": direction_trade_2,
                    "direction_trade_3": direction_trade_3,
                }

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

    def trade_arbitrage(self, req_data):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_name = f"{dir_path}/assets/structured_triangular_pairs.json"
        structure_triangular_pairs_data = get_data_file_json(file_name)
        coin_markets = {}
        price_pairs = []
        for structure_triangular_pair_data in structure_triangular_pairs_data[:2]:
            price = self.__get_price_of_t_pair(
                t_pair=structure_triangular_pair_data,
                coin_markets=coin_markets
            )
            self.__cal_triangular_arb_surface_rate(
                t_pair=structure_triangular_pair_data,
                price_coin=price
            )
        return price_pairs
