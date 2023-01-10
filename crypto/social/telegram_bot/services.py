import json
import logging
import time

from django.conf import settings
from telegram import Update, ForceReply

from crypto.core.utils.dict import get_dict_in_list, get_unique_list_of_dict
from crypto.core.utils.json import get_data_file_json
from crypto.core.utils.string import convert_string_to_money
from crypto.social.telegram_bot.contants import CommandsEnum, Message, MenuTelegram, TimeExchange, \
    CryptoExchange, TypeCryptoExchange, StepBot
from crypto.social.telegram_bot.repository import TelegramRepository
from crypto.tracking.blockchair.services import BlockchairService
from crypto.user.services import UserService

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self, update: Update):
        self.user_service = UserService()
        self.telegram_update = update
        self.telegram_repository = TelegramRepository()
        self.user = None

    def get_message_and_keyboards_by_text_command(self, text_command, **kwargs):
        try:
            logger.info(f"Telegram Service: get_message_and_keyboards_by_text_command with: {text_command}")
            commands = {
                # Step 1
                CommandsEnum.START: lambda: self.get_action_start(**kwargs),
                CommandsEnum.TOKEN: lambda: self.get_action_select_token(**kwargs),
                CommandsEnum.EXCHANGE: lambda: self.get_action_select_exchange(),
                CommandsEnum.ENTER_ADDRESS: lambda: self.get_action_enter_address(**kwargs),
                CommandsEnum.TRIGGER: lambda: self.get_action_trigger(**kwargs),
                # Step 2
                CommandsEnum.TYPE_TOKEN_CRYPTO: lambda: self.get_action_type_crypto_in_crypto_exchange(**kwargs),
                # Step 3
                CommandsEnum.SYMBOL_BINANCE: lambda: self.get_action_select_symbol_binance(**kwargs),
                CommandsEnum.CRYPTO_EXCHANGE: lambda: self.get_action_select_crypto_exchange(**kwargs),
                # Step 4
                CommandsEnum.TIME_EXCHANGE: lambda: self.get_action_get_time_exchange(**kwargs),
                # Step 5 final
                CommandsEnum.ANALYSIS_CRYPTO_DATA: lambda: self.get_action_analysis_crypto_exchange(**kwargs)
            }
            reply_text, reply_keyboard = commands.get(text_command)()
            return reply_text, reply_keyboard
        except Exception as error:
            logger.info(f"Telegram Service: error system with: {str(error)}")
            return Message.UNKNOWN_ERROR, []

    """
    ---------------------------------------------
          Step 1
    --------------------------------------------
    """

    def get_action_start(self, **kwargs):
        logger.info(f"Telegram Service: get_action_start")
        self.user_service.clear_data_user_telegram_tracker()
        reply_text = Message.WELCOME_TEXT
        reply_keyboard = self.telegram_repository.append_to_reply_keyboard(
            MenuTelegram.REPLY_KEYBOARDS.value.get("default"), []
        )
        return reply_text, reply_keyboard

    def get_action_select_token(self, **kwargs):
        logger.info(f"Telegram Service: get_action_select_token")
        file_name = f"{settings.BASE_DIR}/crypto/assets/token_exchange.json"
        tokens_address = get_data_file_json(file_name)
        reply_text = Message.SELECT_TOKEN
        reply_keyboard = self.telegram_repository.create_reply_inline_keyboard(tokens_address,
                                                                               key_name="name",
                                                                               key_callback="symbol")
        self.save_action_user_to_database(
            step_current=StepBot.ONE.value,
            commands=CommandsEnum.TOKEN.value,
            text_input=CommandsEnum.TOKEN.value
        )
        return reply_text, reply_keyboard

    def get_action_select_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_select_exchange")
        reply_text = Message.EXCHANGE
        crypto_exchange = [dict(name=exchange, value=exchange) for exchange in CryptoExchange]
        reply_keyboard = self.telegram_repository.create_reply_inline_keyboard(crypto_exchange,
                                                                               key_name="name",
                                                                               key_callback="value")
        self.save_action_user_to_database(
            step_current=StepBot.ONE.value,
            commands=CommandsEnum.EXCHANGE.value,
            text_input=CommandsEnum.EXCHANGE.value
        )
        return reply_text, reply_keyboard

    def get_action_enter_address(self, **kwargs):
        logger.info(f"Telegram Service: get_action_enter_address")
        reply_text = Message.ENTER_ADDRESS
        self.save_action_user_to_database(
            step_current=StepBot.TWO.value,
            commands=CommandsEnum.ENTER_ADDRESS.value,
            text_input=CommandsEnum.ENTER_ADDRESS.value
        )
        return reply_text, ForceReply(selective=True)

    def get_action_trigger(self, **kwargs):
        logger.info(f"Telegram Service: get_action_enter_address")
        reply_text = Message.TRIGGER_END
        # Todo run trigger
        return reply_text, []

    """
    ---------------------------------------------
          Step 2
    --------------------------------------------
    """

    def get_action_type_crypto_in_crypto_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_select_token_available")
        text = kwargs.get('text')
        reply_text = Message.SELECT_OPTION
        # Todo: validate data
        type_exchange = [
            dict(
                name=type_crypto.name, value=type_crypto.variable
            ) for type_crypto in TypeCryptoExchange
        ]
        reply_keyboard = self.telegram_repository.create_reply_inline_keyboard(type_exchange,
                                                                               key_name="name",
                                                                               key_callback="value")
        self.save_action_user_to_database(
            step_current=StepBot.TWO.value,
            commands=CommandsEnum.TYPE_TOKEN_CRYPTO.value,
            text_input=f'{self.user.get("text_input")}_{text}'
        )
        return reply_text, reply_keyboard

    """
    ---------------------------------------------
          Step 3
    --------------------------------------------
    """

    def get_action_select_symbol_binance(self, **kwargs):
        reply_text = "Please select symbol binance"
        text = kwargs.get("text")
        reply_keyboard_switch = {
            TypeCryptoExchange.SPOT.variable: lambda: self.telegram_repository.get_reply_keyboard_symbol_binance(),
            TypeCryptoExchange.FUTURES.variable: lambda: self.telegram_repository.get_reply_keyboard_symbol_binance(
                is_trade_margin=True
            ),
            TypeCryptoExchange.INPUT_SYMBOL.variable: lambda: self.telegram_repository.create_reply_enter_reply()
        }
        self.save_action_user_to_database(
            step_current=StepBot.THREE.value,
            commands=CommandsEnum.SYMBOL_BINANCE.value,
            text_input=f'{self.user.get("text_input")}_{text}'
        )
        reply_keyboard = reply_keyboard_switch.get(text)()
        return reply_text, reply_keyboard

    def get_action_select_crypto_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_select_crypto_exchange")
        information_exchange_text = kwargs.get("text")
        reply_text = Message.SELECT_CRYPTO_EXCHANGE
        file_name = f"{settings.BASE_DIR}/crypto/assets/crypto_exchange_address.json"
        crypto_exchanges = get_data_file_json(file_name)
        exchange_data = [dict(
            exchange=crypto_exchange.get("exchange"),
            exchange_id=crypto_exchange.get('exchange_id')
        ) for crypto_exchange in crypto_exchanges]
        exchange_data = get_unique_list_of_dict(exchange_data)
        exchange_data.append(dict(
            exchange=CommandsEnum.ALL,
            exchange_id=CommandsEnum.ALL.value
        ))
        reply_keyboard = self.telegram_repository.create_reply_inline_keyboard(exchange_data,
                                                                               key_name="exchange",
                                                                               key_callback="exchange_id")
        self.save_action_user_to_database(
            step_current=StepBot.THREE.value,
            commands=CommandsEnum.CRYPTO_EXCHANGE.value,
            text_input=f'{self.user.get("text_input")}_{information_exchange_text}'
        )
        return reply_text, reply_keyboard

    """
    ---------------------------------------------
          Step 4
    --------------------------------------------
    """

    def get_action_get_time_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_get_time_exchange")
        crypto_exchange_select = kwargs.get("text")
        reply_text = Message.SELECT_TIME_EXCHANGE
        times = [dict(
            time=time_exchange.name,
            keyword=str(time_exchange.minutes)
        ) for time_exchange in TimeExchange]
        reply_keyboard = self.telegram_repository.create_reply_inline_keyboard(times,
                                                                               key_name="time",
                                                                               key_callback="keyword")

        self.save_action_user_to_database(
            step_current=StepBot.FOUR.value,
            commands=CommandsEnum.TIME_EXCHANGE.value,
            text_input=f'{self.user.get("text_input")}_{crypto_exchange_select}'
        )
        return reply_text, reply_keyboard

    """
    ---------------------------------------------
          Step 5 Final
    --------------------------------------------
    """

    def get_action_analysis_crypto_exchange(self, **kwargs):
        logger.info(f"Telegram Service: get_action_analysis_crypto_exchange")
        time_ago = kwargs.get("text")
        exchange_id, address_token = self.telegram_repository.get_info_data_by_user(user=self.user)
        response_data = []
        if CommandsEnum.ALL in exchange_id:
            file_name = f"{settings.BASE_DIR}/crypto/assets/crypto_exchange_address.json"
            crypto_exchanges = get_data_file_json(file_name)
            crypto_exchanges = get_unique_list_of_dict(crypto_exchanges)
        else:
            crypto_exchanges = [dict(exchange_id=exchange_id)]

        for crypto_exchange in crypto_exchanges:
            req_data = {
                "token_address": address_token,
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
          Connection database
    --------------------------------------------
    """

    def save_action_user_to_database(self, step_current, commands, text_input):
        logger.info(f"Telegram Service: save_action_user_to_database {step_current} - {commands} - {text_input}")
        user_id = self.telegram_update.message.chat.id
        user = self.user_service.get_user_telegram_tracker_by_user_id(user_id)
        if user and "error" in user.keys():
            logger.info(f"Save action user to database")
            raise ValueError("Not create data tracker")

        req_data = {
            'user_id': str(user_id),
            'username': self.telegram_update.message.chat.username,
            'step_current': int(step_current),
            'commands': str(commands),
            'text_input': text_input
        }
        if not user:
            self.user_service.create_action_tracking_telegram(req_data=req_data)
        else:
            self.user_service.update_user_telegram_tracker_by_user_id(user_id=user_id, req_data=req_data)

    def get_action_user_from_database(self):
        user = self.user_service.get_user_telegram_tracker_by_user_id(
            user_id=self.telegram_update.message.chat.id
        )
        if user and "error" in user.keys():
            raise ValueError("Get user from database failed")

        self.user = user
        return user

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
