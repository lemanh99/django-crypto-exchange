import logging

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from telegram import Update, ForceReply, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from crypto.social.telegram_bot.contants import Message, CommandsEnum, MenuTelegram
from crypto.social.telegram_bot.services import TelegramService

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def remove_chat_buttons(bot, chat_id: int, text: str):
    """Deletes buttons below the chat.
    For now there are no way to delete kbd other than inline one, check
        https://core.telegram.org/bots/api#updating-messages.
    """
    bot.send_message(chat_id, text=text, reply_markup=ReplyKeyboardRemove())


def error(update, context):
    logger.info('Update "%s" caused error "%s"', update, context.error)


def echo(update: Update, _: CallbackContext) -> None:
    logger.info("Run echo")
    """Echo the user message."""
    text = update.message.text
    logger.info(f"Select text:{text}")
    reply_text = ""
    reply_keyboard = MenuTelegram.REPLY_KEYBOARDS.value.get("default")
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, )
    text = text.replace(CommandsEnum.BACK_BUTTON_PRETEXT, "")
    telegram_service = TelegramService(update=update)
    user = telegram_service.get_action_user_from_database()
    """
    ---------------------------------------------
          Step 1
    --------------------------------------------
    """
    if text in [CommandsEnum.START, '/start']:
        user = update.message.from_user
        logger.info("User %s started the conversation.", user.first_name)
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.START
        )
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, )

    elif text == CommandsEnum.HELP:
        reply_text = Message.HELP_TEXT

    elif text == CommandsEnum.CANCEL:
        remove_chat_buttons(update.message.bot, update.message.chat_id, text=Message.GOODBYE)

    elif text in [CommandsEnum.TOKEN, '/token']:
        remove_chat_buttons(bot=update.message.bot, chat_id=update.message.chat_id, text="Hi !!")
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.TOKEN
        )
        reply_markup = InlineKeyboardMarkup(reply_keyboard)

    elif text in [CommandsEnum.EXCHANGE, '/exchange']:
        remove_chat_buttons(bot=update.message.bot, chat_id=update.message.chat_id, text="Hi !!")
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.EXCHANGE
        )
        reply_markup = InlineKeyboardMarkup(reply_keyboard)

    elif text in [CommandsEnum.ADDRESS, '/address']:
        remove_chat_buttons(bot=update.message.bot, chat_id=update.message.chat_id, text='Hi !!')
        reply_text, reply_markup = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.ENTER_ADDRESS
        )
    elif text in [CommandsEnum.TRIGGER, '/trigger']:
        remove_chat_buttons(bot=update.message.bot, chat_id=update.message.chat_id, text="Hi !!")
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.TRIGGER
        )
        reply_markup = InlineKeyboardMarkup(reply_keyboard)

    elif user and (
            user.get('commands') == CommandsEnum.SYMBOL_BINANCE or user.get('commands') == CommandsEnum.ENTER_ADDRESS
    ):
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.CRYPTO_EXCHANGE, text=text
        )
        reply_markup = InlineKeyboardMarkup(reply_keyboard)


    else:
        reply_text = Message.UNKNOWN_COMMAND.format(text=text)

    update.message.reply_text(
        reply_text,
        reply_markup=reply_markup
    )


def callback_echo(update, context):
    query = update.callback_query
    query_data = query.data
    logger.info(f"callback_echo {query_data}")
    logger.info(f"Debug: Data callback {query}")
    telegram_service = TelegramService(update=update.callback_query)

    """
    ---------------------------------------------
          Step 2 callback
    --------------------------------------------
    """
    try:
        user = telegram_service.get_action_user_from_database()
        commands_before = user.get('commands')
        # Type exchange
        if commands_before == CommandsEnum.EXCHANGE:
            if telegram_service.is_crypto_exchange_available(text=query_data):
                reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
                    text_command=CommandsEnum.TYPE_TOKEN_CRYPTO, text=query_data
                )
                reply_markup = InlineKeyboardMarkup(reply_keyboard)
                query.edit_message_text(text=f"You have selected {query_data}, {reply_text}", reply_markup=reply_markup)
            else:
                query.edit_message_text(text=f"Please select again", reply_markup=None)

        elif commands_before == CommandsEnum.TYPE_TOKEN_CRYPTO:
            reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
                text_command=CommandsEnum.SYMBOL_BINANCE, text=query_data
            )
            reply_markup = InlineKeyboardMarkup(reply_keyboard)
            query.edit_message_text(text=f"You have selected {query_data}, {reply_text}", reply_markup=reply_markup)
        elif commands_before == CommandsEnum.SYMBOL_BINANCE:
            reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
                text_command=CommandsEnum.CRYPTO_EXCHANGE, text=query_data
            )
            reply_markup = InlineKeyboardMarkup(reply_keyboard)
            query.edit_message_text(text=f"You have selected {query_data}, {reply_text}", reply_markup=reply_markup)

        # Type token
        elif commands_before == CommandsEnum.TOKEN:
            reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
                text_command=CommandsEnum.CRYPTO_EXCHANGE, text=query_data
            )
            reply_markup = InlineKeyboardMarkup(reply_keyboard)
            query.edit_message_text(text=f"You have selected {query_data}", reply_markup=reply_markup)

        elif commands_before == CommandsEnum.CRYPTO_EXCHANGE:
            reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
                text_command=CommandsEnum.TIME_EXCHANGE, text=query_data
            )
            reply_markup = InlineKeyboardMarkup(reply_keyboard)
            query.edit_message_text(text=f"You have selected {query_data}, {reply_text}",
                                    reply_markup=reply_markup)
        elif commands_before == CommandsEnum.TIME_EXCHANGE:
            query.edit_message_text(text=f"Waiting ...")
            data_analysis, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
                text_command=CommandsEnum.ANALYSIS_CRYPTO_DATA, text=query_data
            )
            query.edit_message_text(text=f"Information transaction")
            template = get_template("telegram/information_analysis_data.html")
            for data in data_analysis:
                render_context = Context(dict(**data))
                html = template.template.render(render_context)
                context.bot.send_message(chat_id=query.message.chat.id, text=str(html), parse_mode='HTML')

            query.edit_message_text(text=f"You select exchange {query_data}", parse_mode='HTML')
        else:
            query.answer(text=f"Please select again !")
    except Exception as e:
        logger.info("Callback error: %s", str(e))
        query.edit_message_text(text=f"Please select again", reply_markup=None)


def run_telegram_bot_v2() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    try:
        logger.info("Start run telegram bot")
        updater = Updater(settings.TELEGRAM_BOT_API_KEY, use_context=True)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram

        # on non command i.e message - echo the message on Telegram
        dispatcher.add_handler(MessageHandler(Filters.text, echo))
        dispatcher.add_handler(CallbackQueryHandler(callback_echo))

        # log all errors
        dispatcher.add_error_handler(error)
        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
        logger.info("End run telegram bot")
    except Exception as e:
        logger.info("Run telegram bot error: " + str(e))
