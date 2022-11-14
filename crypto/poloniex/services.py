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

        # Set Variables
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

        # Extract Pair Variables
        a_base = t_pair["a_base"]
        a_quote = t_pair["a_quote"]
        b_base = t_pair["b_base"]
        b_quote = t_pair["b_quote"]
        c_base = t_pair["c_base"]
        c_quote = t_pair["c_quote"]
        pair_a = t_pair["pair_a"]
        pair_b = t_pair["pair_b"]
        pair_c = t_pair["pair_c"]

        # Extract Price Information
        a_ask = price_coin["pair_a_ask"]
        a_bid = price_coin["pair_a_bid"]
        b_ask = price_coin["pair_b_ask"]
        b_bid = price_coin["pair_b_bid"]
        c_ask = price_coin["pair_c_ask"]
        c_bid = price_coin["pair_c_bid"]

        # Set directions and loop through
        direction_list = ["forward", "reverse"]
        for direction in direction_list:

            # Set additional variables for swap information
            swap_1 = 0
            swap_2 = 0
            swap_3 = 0
            swap_1_rate = 0
            swap_2_rate = 0
            swap_3_rate = 0

            """
                Poloniex Rules !!
                If we are swapping the coin on the left (Base) to the right (Quote) then * (1 / Ask)
                If we are swapping the coin on the right (Quote) to the left (Base) then * Bid
            """

            # Assume starting with a_base and swapping for a_quote
            if direction == "forward":
                swap_1 = a_base
                swap_2 = a_quote
                swap_1_rate = 1 / a_ask
                direction_trade_1 = "base_to_quote"

            # Assume starting with a_base and swapping for a_quote
            if direction == "reverse":
                swap_1 = a_quote
                swap_2 = a_base
                swap_1_rate = a_bid
                direction_trade_1 = "quote_to_base"

            # Place first trade
            contract_1 = pair_a
            acquired_coin_t1 = starting_amount * swap_1_rate

            """  FORWARD """
            # SCENARIO 1 Check if a_quote (acquired_coin) matches b_quote
            if direction == "forward":
                if a_quote == b_quote and calculated == 0:
                    swap_2_rate = b_bid
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "quote_to_base"
                    contract_2 = pair_b

                    # If b_base (acquired coin) matches c_base
                    if b_base == c_base:
                        swap_3 = c_base
                        swap_3_rate = 1 / c_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_c

                    # If b_base (acquired coin) matches c_quote
                    if b_base == c_quote:
                        swap_3 = c_quote
                        swap_3_rate = c_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_c

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

                # SCENARIO 2 Check if a_quote (acquired_coin) matches b_base
                if a_quote == b_base and calculated == 0:
                    swap_2_rate = 1 / b_ask
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "base_to_quote"
                    contract_2 = pair_b

                    # If b_quote (acquired coin) matches c_base
                    if b_quote == c_base:
                        swap_3 = c_base
                        swap_3_rate = 1 / c_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_c

                    # If b_quote (acquired coin) matches c_quote
                    if b_quote == c_quote:
                        swap_3 = c_quote
                        swap_3_rate = c_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_c

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

                # SCENARIO 3 Check if a_quote (acquired_coin) matches c_quote
                if a_quote == c_quote and calculated == 0:
                    swap_2_rate = c_bid
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "quote_to_base"
                    contract_2 = pair_c

                    # If c_base (acquired coin) matches b_base
                    if c_base == b_base:
                        swap_3 = b_base
                        swap_3_rate = 1 / b_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_b

                    # If c_base (acquired coin) matches b_quote
                    if c_base == b_quote:
                        swap_3 = b_quote
                        swap_3_rate = b_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_b

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

                # SCENARIO 4 Check if a_quote (acquired_coin) matches c_base
                if a_quote == c_base and calculated == 0:
                    swap_2_rate = 1 / c_ask
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "base_to_quote"
                    contract_2 = pair_c

                    # If c_quote (acquired coin) matches b_base
                    if c_quote == b_base:
                        swap_3 = b_base
                        swap_3_rate = 1 / b_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_b

                    # If c_quote (acquired coin) matches b_quote
                    if c_quote == b_quote:
                        swap_3 = b_quote
                        swap_3_rate = b_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_b

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

            """  REVERSE """
            # SCENARIO 1 Check if a_base (acquired_coin) matches b_quote
            if direction == "reverse":
                if a_base == b_quote and calculated == 0:
                    swap_2_rate = b_bid
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "quote_to_base"
                    contract_2 = pair_b

                    # If b_base (acquired coin) matches c_base
                    if b_base == c_base:
                        swap_3 = c_base
                        swap_3_rate = 1 / c_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_c

                    # If b_base (acquired coin) matches c_quote
                    if b_base == c_quote:
                        swap_3 = c_quote
                        swap_3_rate = c_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_c

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

                # SCENARIO 2 Check if a_base (acquired_coin) matches b_base
                if a_base == b_base and calculated == 0:
                    swap_2_rate = 1 / b_ask
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "base_to_quote"
                    contract_2 = pair_b

                    # If b_quote (acquired coin) matches c_base
                    if b_quote == c_base:
                        swap_3 = c_base
                        swap_3_rate = 1 / c_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_c

                    # If b_quote (acquired coin) matches c_quote
                    if b_quote == c_quote:
                        swap_3 = c_quote
                        swap_3_rate = c_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_c

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

                # SCENARIO 3 Check if a_base (acquired_coin) matches c_quote
                if a_base == c_quote and calculated == 0:
                    swap_2_rate = c_bid
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "quote_to_base"
                    contract_2 = pair_c

                    # If c_base (acquired coin) matches b_base
                    if c_base == b_base:
                        swap_3 = b_base
                        swap_3_rate = 1 / b_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_b

                    # If c_base (acquired coin) matches b_quote
                    if c_base == b_quote:
                        swap_3 = b_quote
                        swap_3_rate = b_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_b

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

            # SCENARIO 4 Check if a_base (acquired_coin) matches c_base
            if direction == "reverse":
                if a_base == c_base and calculated == 0:
                    swap_2_rate = 1 / c_ask
                    acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                    direction_trade_2 = "base_to_quote"
                    contract_2 = pair_c

                    # If c_quote (acquired coin) matches b_base
                    if c_quote == b_base:
                        swap_3 = b_base
                        swap_3_rate = 1 / b_ask
                        direction_trade_3 = "base_to_quote"
                        contract_3 = pair_b

                    # If c_quote (acquired coin) matches b_quote
                    if c_quote == b_quote:
                        swap_3 = b_quote
                        swap_3_rate = b_bid
                        direction_trade_3 = "quote_to_base"
                        contract_3 = pair_b

                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                    calculated = 1

            """ PROFIT LOSS OUTPUT """

            # Profit and Loss Calculations
            profit_loss = acquired_coin_t3 - starting_amount
            profit_loss_perc = (profit_loss / starting_amount) * 100 if profit_loss != 0 else 0

            # Trade Descriptions
            trade_description_1 = f"Start with {swap_1} of {starting_amount}. Swap at {swap_1_rate} for {swap_2} acquiring {acquired_coin_t1}."
            trade_description_2 = f"Swap {acquired_coin_t1} of {swap_2} at {swap_2_rate} for {swap_3} acquiring {acquired_coin_t2}."
            trade_description_3 = f"Swap {acquired_coin_t2} of {swap_3} at {swap_3_rate} for {swap_1} acquiring {acquired_coin_t3}."

            # Output Results
            if profit_loss_perc > min_surface_rate:
                surface_dict = {
                    "swap_1": swap_1,
                    "swap_2": swap_2,
                    "swap_3": swap_3,
                    "contract_1": contract_1,
                    "contract_2": contract_2,
                    "contract_3": contract_3,
                    "direction_trade_1": direction_trade_1,
                    "direction_trade_2": direction_trade_2,
                    "direction_trade_3": direction_trade_3,
                    "starting_amount": starting_amount,
                    "acquired_coin_t1": acquired_coin_t1,
                    "acquired_coin_t2": acquired_coin_t2,
                    "acquired_coin_t3": acquired_coin_t3,
                    "swap_1_rate": swap_1_rate,
                    "swap_2_rate": swap_2_rate,
                    "swap_3_rate": swap_3_rate,
                    "profit_loss": profit_loss,
                    "profit_loss_perc": profit_loss_perc,
                    "direction": direction,
                    "trade_description_1": trade_description_1,
                    "trade_description_2": trade_description_2,
                    "trade_description_3": trade_description_3
                }

                return surface_dict

        return surface_dict

    def __calculate_acquired_coin(self, amount_in, orderbook):

        """
            CHALLENGES
            Full amount of starting amount can be eaten on the first level (level 0)
            Some of the amount in can be eaten up by multiple levels
            Some coins may not have enough liquidity
        """

        # Initialise Variables
        trading_balance = amount_in
        quantity_bought = 0
        acquired_coin = 0
        counts = 0
        for level in orderbook:

            # Extract the level price and quantity
            level_price = level[0]
            level_available_quantity = level[1]

            amount_bought = 0
            # Amount In is <= first level total amount
            if trading_balance <= level_available_quantity:
                quantity_bought = trading_balance
                trading_balance = 0
                amount_bought = quantity_bought * level_price

            # Amount In is > a given level total amount
            if trading_balance > level_available_quantity:
                quantity_bought = level_available_quantity
                trading_balance -= quantity_bought
                amount_bought = quantity_bought * level_price

            # Accumulate Acquired Coin
            acquired_coin = acquired_coin + amount_bought

            # Exit Trade
            if trading_balance == 0:
                return acquired_coin

            # Exit if not enough order book levels
            counts += 1
            if counts == len(orderbook):
                return 0

    def __reformat_orderbook(self, prices, c_direction):
        price_list_main = []
        if c_direction == "base_to_quote":
            asks_list = prices["asks"]
            for price, quantity in zip(asks_list[::2], asks_list[1::2]):
                ask_price = float(price)
                adj_price = 1 / ask_price if ask_price != 0 else 0
                adj_quantity = float(quantity) * ask_price
                price_list_main.append([adj_price, adj_quantity])
        if c_direction == "quote_to_base":
            bids_list = prices["bids"]
            for price, quantity in zip(bids_list[::2], bids_list[1::2]):
                bid_price = float(price)
                adj_price = bid_price if bid_price != 0 else 0
                adj_quantity = float(quantity)
                price_list_main.append([adj_price, adj_quantity])

        return price_list_main

    # Get the Depth From the Order Book
    def __get_depth_from_orderbook(self, surface_arb, coin_markets):

        # Extract initial variables
        swap_1 = surface_arb["swap_1"]
        starting_amount = 100
        starting_amount_dict = {
            "USDT": 100,
            "USDC": 100,
            "BTC": 0.05,
            "ETH": 0.1
        }
        if swap_1 in starting_amount_dict:
            starting_amount = starting_amount_dict[swap_1]

        # Define pairs
        contract_1 = surface_arb["contract_1"]
        contract_2 = surface_arb["contract_2"]
        contract_3 = surface_arb["contract_3"]

        # Define direction for trades
        contract_1_direction = surface_arb["direction_trade_1"]
        contract_2_direction = surface_arb["direction_trade_2"]
        contract_3_direction = surface_arb["direction_trade_3"]

        depth_1_reformatted_prices = self.__reformat_orderbook(
            prices=coin_markets[contract_1],
            c_direction=contract_1_direction
        )
        depth_2_reformatted_prices = self.__reformat_orderbook(
            prices=coin_markets[contract_2],
            c_direction=contract_2_direction
        )
        depth_3_reformatted_prices = self.__reformat_orderbook(
            prices=coin_markets[contract_3],
            c_direction=contract_3_direction
        )

        # Get Acquired Coins
        acquired_coin_t1 = self.__calculate_acquired_coin(starting_amount, depth_1_reformatted_prices)
        acquired_coin_t2 = self.__calculate_acquired_coin(acquired_coin_t1, depth_2_reformatted_prices)
        acquired_coin_t3 = self.__calculate_acquired_coin(acquired_coin_t2, depth_3_reformatted_prices)

        # Calculate Profit Loss Also Known As Real Rate
        profit_loss = acquired_coin_t3 - starting_amount
        real_rate_perc = (profit_loss / starting_amount) * 100 if profit_loss != 0 else 0

        if real_rate_perc > -1:
            return_dict = {
                "profit_loss": profit_loss,
                "real_rate_perc": real_rate_perc,
                "price_except": f"{starting_amount}({swap_1})->{round(real_rate_perc * real_rate_perc / 100, 4)}({swap_1})",
                "contract_1": contract_1,
                "contract_2": contract_2,
                "contract_3": contract_3,
                "contract_1_direction": contract_1_direction,
                "contract_2_direction": contract_2_direction,
                "contract_3_direction": contract_3_direction
            }
            return return_dict
        else:
            return {}

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
        for structure_triangular_pair_data in structure_triangular_pairs_data:
            price_coins = self.__get_price_of_t_pair(
                t_pair=structure_triangular_pair_data,
                coin_markets=coin_markets
            )
            surface_arb = self.__cal_triangular_arb_surface_rate(
                t_pair=structure_triangular_pair_data,
                price_coin=price_coins
            )
            if surface_arb:
                real_rate_arb = self.__get_depth_from_orderbook(surface_arb, coin_markets)
                price_pairs.append(real_rate_arb)

        return price_pairs
