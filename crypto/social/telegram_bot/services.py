import json
import logging

from django.conf import settings
from djoser.utils import encode_uid
from telegram import InlineKeyboardButton

from crypto.core.utils.dict import get_dict_in_list, get_unique_list_of_dict
from crypto.core.utils.json import get_data_file_json, convert_json_to_string
from crypto.core.utils.string import convert_string_to_money
from crypto.social.telegram_bot.contants import CommandsEnum, Position, Message, MenuTelegram, TimeExchange, \
    CryptoExchange, TypeCryptoExchange, StepBot
from crypto.tracking.blockchair.services import BlockchairService

logger = logging.getLogger(__name__)


class TelegramService:

    def get_message_and_keyboards_by_text_command(self, text_command, **kwargs):
        logger.info(f"Telegram Service: get_message_and_keyboards_by_text_command with: {text_command}")
        commands = {
            # Step 1
            CommandsEnum.START: lambda: self.get_action_start(**kwargs),
            CommandsEnum.TOKEN: lambda: self.get_action_select_token(**kwargs),
            CommandsEnum.EXCHANGE: lambda: self.get_action_select_exchange(),
            CommandsEnum.TYPE_TOKEN_CRYPTO: lambda: self.get_action_type_crypto_in_crypto_exchange(**kwargs),
            # CommandsEnum.CRYPTO_EXCHANGE: lambda: self.get_action_select_crypto_exchange(**kwargs),
            # CommandsEnum.TIME_EXCHANGE: lambda: self.get_action_get_time_exchange(**kwargs),
            # CommandsEnum.ANALYSIS_CRYPTO_DATA: lambda: self.get_action_analysis_crypto_exchange(**kwargs)
        }
        reply_text, reply_keyboard = commands.get(text_command)()
        return reply_text, reply_keyboard

    """
    ---------------------------------------------
          Step 1
    --------------------------------------------
    """

    def get_action_start(self, **kwargs):
        logger.info(f"Telegram Service: get_action_start")
        reply_text = Message.WELCOME_TEXT
        reply_keyboard = self.append_to_reply_keyboard(MenuTelegram.REPLY_KEYBOARDS.value.get("default"), [])
        return reply_text, reply_keyboard

    def get_action_select_token(self, **kwargs):
        logger.info(f"Telegram Service: get_action_select_token")
        file_name = f"{settings.BASE_DIR}/crypto/assets/token_exchange.json"
        tokens_address = get_data_file_json(file_name)
        reply_text = Message.SELECT_TOKEN
        reply_keyboard = self.create_reply_inline_keyboard(tokens_address, key_name="name", key_callback="symbol")
        return reply_text, reply_keyboard

    def get_action_select_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_select_exchange")
        reply_text = Message.EXCHANGE
        crypto_exchange = [dict(name=exchange, value=exchange) for exchange in CryptoExchange]
        reply_keyboard = self.create_reply_inline_keyboard(crypto_exchange, key_name="name", key_callback="value")
        return reply_text, reply_keyboard

    """
    ---------------------------------------------
          Step 2
    --------------------------------------------
    """

    def get_action_type_crypto_in_crypto_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_select_token_available")
        text = kwargs.get('text')
        key_callback = {
            "step_current": StepBot.TWO.value,
            "step_1": text,
            "step_2": ""
        }
        type_exchange = []
        for type_crypto in TypeCryptoExchange:
            key_callback.update(step_2=type_crypto.variable)
            s = convert_json_to_string(key_callback)
            text = encode_uid(s)
            type_exchange.append(dict(
                name=type_crypto.name, value=text
            ))

        reply_text = Message.SELECT_OPTION
        reply_keyboard = self.create_reply_inline_keyboard(type_exchange, key_name="name", key_callback="value")
        return reply_text, reply_keyboard

    def get_action_select_token_available_in_crypto_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_select_token_available")
        information_exchange_text = kwargs.get("text")
        reply_text = Message.SELECT_CRYPTO_EXCHANGE
        reply_keyboard = []
        return reply_text, reply_keyboard

    def get_action_select_crypto_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_select_crypto_exchange")
        information_exchange_text = kwargs.get("text")
        reply_text = Message.SELECT_CRYPTO_EXCHANGE
        file_name = f"{settings.BASE_DIR}/crypto/assets/crypto_exchange_address.json"
        crypto_exchanges = get_data_file_json(file_name)
        exchange_data = [dict(
            exchange=crypto_exchange.get("exchange"),
            exchange_id=json.dumps(dict(layer_1=information_exchange_text, layer_2=crypto_exchange.get('exchange_id')))
        ) for crypto_exchange in crypto_exchanges]
        exchange_data = get_unique_list_of_dict(exchange_data)
        exchange_data.append(dict(
            exchange=CommandsEnum.ALL,
            exchange_id=f"{information_exchange_text}_{CommandsEnum.ALL}"
        ))
        reply_keyboard = self.create_reply_inline_keyboard(exchange_data,
                                                           key_name="exchange",
                                                           key_callback="exchange_id")
        return reply_text, reply_keyboard

    def get_action_get_time_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_get_time_exchange")
        symbol_token = kwargs.get("text")
        reply_text = Message.SELECT_TIME_EXCHANGE
        times = [dict(
            time=time_exchange.name,
            keyword=f"{symbol_token}_{str(time_exchange.minutes)}"
        ) for time_exchange in TimeExchange]
        reply_keyboard = self.create_reply_inline_keyboard(times,
                                                           key_name="time",
                                                           key_callback="keyword")
        return reply_text, reply_keyboard

    def get_action_analysis_crypto_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_analysis_crypto_exchange")
        text = kwargs.get("text")
        symbol_token, exchange_id, time_ago = text.split("_")[0], text.split("_")[1], text.split("_")[2]
        file_name = f"{settings.BASE_DIR}/crypto/assets/token_exchange.json"
        tokens_address = get_data_file_json(file_name)
        token = get_dict_in_list(key="symbol", value=symbol_token, my_dictlist=tokens_address)
        response_data = []
        if CommandsEnum.ALL in exchange_id:
            file_name = f"{settings.BASE_DIR}/crypto/assets/crypto_exchange_address.json"
            crypto_exchanges = get_data_file_json(file_name)
        else:
            crypto_exchanges = [dict(exchange_id=exchange_id)]

        for crypto_exchange in crypto_exchanges:
            req_data = {
                "token_address": token.get("address"),
                "exchange_id": crypto_exchange.get("exchange_id"),
                "min_order_exchange": 50000,
                "time_ago": int(time_ago),
            }
            data = self.get_data_analysis_crypto_exchange(req_data)
            response_data.extend(data)
        return response_data, None

    @classmethod
    def get_data_analysis_crypto_exchange(cls, req_data):
        blockchair = BlockchairService()
        data_analysis = blockchair.get_analysis_token_by_exchange(req_data)
        response_data = []
        for data in data_analysis:
            response_data.append(dict(
                price_token=data.get("price_token"),
                name_exchange=data.get("name_exchange"),
                value_exchange=convert_string_to_money(data.get("value_exchange", 0)),
                value_in_exchange=convert_string_to_money(data.get("value_in_exchange", 0)),
                value_out_exchange=convert_string_to_money(data.get("value_out_exchange", 0)),
                number_in_exchange=data.get("number_in_exchange"),
                number_out_exchange=data.get("number_out_exchange"),
                value_big_order=data.get("value_big_order"),
                value_in_big_order=data.get("value_in_big_order"),
                number_in_big_order=data.get("number_in_big_order"),
                value_out_big_order=data.get("value_out_big_order"),
                number_out_big_order=data.get("number_out_big_order"),
                datetime_to=data.get("datetime_to"),
                datetime_from=data.get("datetime_from"),
            ))
        return response_data

    """
    ---------------------------------------------
          Check condition step
    --------------------------------------------
    """

    @staticmethod
    def is_crypto_exchange_available(**kwargs):
        text = kwargs.get("text")
        return text in [exchange for exchange in CryptoExchange]

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
