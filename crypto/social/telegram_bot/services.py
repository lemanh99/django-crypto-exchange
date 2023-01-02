from django.conf import settings
from telegram import InlineKeyboardButton

from crypto.core.utils.dict import get_list_in_dict_by_key, get_dict_in_list
from crypto.core.utils.json import get_data_file_json
from crypto.social.telegram_bot.contants import CommandsEnum, Position, Message, MenuTelegram
from crypto.tracking.blockchair.services import BlockchairService


class TelegramService:

    def get_message_and_keyboards_by_text_command(self, text_command, **kwargs):
        print(f"Telegram Service: get_message_and_keyboards_by_text_command with: {text_command}")
        commands = {
            CommandsEnum.START: lambda: self.get_action_start(**kwargs),
            CommandsEnum.TOKEN: lambda: self.get_action_select_token(**kwargs),
            CommandsEnum.CRYPTO_EXCHANGE: lambda: self.get_action_select_crypto_exchange(**kwargs),
            CommandsEnum.ANALYSIS_CRYPTO_DATA: lambda: self.get_action_analysis_crypto_exchange(**kwargs)
        }
        reply_text, reply_keyboard = commands.get(text_command)()
        return reply_text, reply_keyboard

    def get_action_start(self, **kwargs):
        reply_text = Message.WELCOME_TEXT
        reply_keyboard = self.append_to_reply_keyboard(MenuTelegram.REPLY_KEYBOARDS.value.get("default"), [])
        return reply_text, reply_keyboard

    def get_action_select_token(self, **kwargs):
        file_name = f"{settings.BASE_DIR}/crypto/assets/token_exchange.json"
        tokens_address = get_data_file_json(file_name)
        reply_text = Message.SELECT_TOKEN
        reply_keyboard = self.create_reply_inline_keyboard(tokens_address, key_name="name", key_callback="symbol")
        return reply_text, reply_keyboard

    def get_action_select_crypto_exchange(self, **kwargs):
        symbol_token = kwargs.get("text")
        reply_text = Message.SELECT_CRYPTO_EXCHANGE
        file_name = f"{settings.BASE_DIR}/crypto/assets/crypto_exchange_address.json"
        crypto_exchanges = get_data_file_json(file_name)
        exchange_data = [dict(
            exchange=crypto_exchange.get("exchange"),
            exchange_id=f"{symbol_token.lower()}_{crypto_exchange.get('exchange_id')}"
        ) for crypto_exchange in crypto_exchanges]
        reply_keyboard = self.create_reply_inline_keyboard(exchange_data,
                                                           key_name="exchange",
                                                           key_callback="exchange_id")
        return reply_text, reply_keyboard

    def get_action_analysis_crypto_exchange(self, **kwargs):
        text = kwargs.get("text")
        symbol_token, exchange_id = text.split("_")[0], text.split("_")[1]
        file_name = f"{settings.BASE_DIR}/crypto/assets/token_exchange.json"
        tokens_address = get_data_file_json(file_name)
        token = get_dict_in_list(key="symbol", value=symbol_token, my_dictlist=tokens_address)
        req_data = {
            "token_address": token.get("address"),
            "exchange_id": exchange_id
        }
        blockchair = BlockchairService()
        reply_text = blockchair.get_analysis_token_by_exchange(req_data)
        return reply_text, []

    @staticmethod
    def is_token_address_available(**kwargs):
        file_name = f"{settings.BASE_DIR}/crypto/assets/token_exchange.json"
        tokens_address = get_data_file_json(file_name)
        token_info = get_dict_in_list(
            key="symbol",
            value=kwargs.get("text"),
            my_dictlist=tokens_address
        )
        if not token_info:
            return False

        return True

    @staticmethod
    def create_reply_keyboard(options: list) -> list:
        return [[option] for option in options]

    @staticmethod
    def create_reply_inline_keyboard(options: list, key_name: str, key_callback: str) -> list:
        return [[
            InlineKeyboardButton(option.get(key_name), callback_data=option.get(key_callback))
        ] for option in options]

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