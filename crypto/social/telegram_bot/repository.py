from telegram import InlineKeyboardButton, ForceReply

from crypto.coingecko.services import CoinGeckoService
from crypto.social.telegram_bot.contants import Position, CommandsEnum


class TelegramRepository:
    def __init__(self):
        self.coingecko = CoinGeckoService()

    @staticmethod
    def create_reply_inline_keyboard(options: list, key_name: str, key_callback: str) -> list:
        return [[
            InlineKeyboardButton(option.get(key_name), callback_data=option.get(key_callback))
        ] for option in options]

    @staticmethod
    def create_reply_inline_multiple_keyboard(options: list, key_name: str, key_callback: str) -> list:
        number_in_row = 6
        number_row = round(len(options) / number_in_row) + 1
        inline_keyboards = []
        for row in range(1, number_row + 1):
            option_rows = options[number_in_row * row - number_in_row: number_in_row * row]
            inline_keyboards.append([
                InlineKeyboardButton(option.get(key_name), callback_data=option.get(key_callback))
                for option in option_rows
            ])
        return inline_keyboards

    @staticmethod
    def create_reply_keyboard(options: list) -> list:
        return [[option] for option in options]

    @classmethod
    def append_to_reply_keyboard(cls, reply_keyboard, options: list, position=Position.TOP) -> list:
        # Appending options to reply keyboard.
        if not options:
            return reply_keyboard
        new_keyboard_options = cls.create_reply_keyboard(options)
        if position == Position.TOP:
            return new_keyboard_options + reply_keyboard
        else:
            return reply_keyboard + new_keyboard_options

    @classmethod
    def append_back_button(cls, reply_keyboard, text, position=Position.TOP):
        button_text = CommandsEnum.BACK_BUTTON_PRETEXT + text
        return cls.append_to_reply_keyboard(reply_keyboard, [button_text], position)

    @classmethod
    def create_reply_enter_reply(cls):
        return []

    def get_reply_keyboard_symbol_binance(self, is_trade_margin=False):
        platform = "ethereum"
        req_data = {
            "trade_margin": is_trade_margin,
            "platform": platform
        }
        token_address_info = self.coingecko.get_address_token_by_exchange_id(
            exchange_id='binance', req_data=req_data
        )
        data_keyboard = [dict(
            name=token_address.get("binance_symbol"),
        ) for token_address in token_address_info]
        reply_keyboard = self.create_reply_inline_multiple_keyboard(data_keyboard,
                                                                    key_name="name",
                                                                    key_callback="name")
        return reply_keyboard
