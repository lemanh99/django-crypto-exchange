import logging

from django.conf import settings
from telegram import Update, ForceReply, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from crypto.social.telegram_bot.contants import Message, CommandsEnum, MenuTelegram
from crypto.social.telegram_bot.services import TelegramService

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


def echo(update: Update, _: CallbackContext) -> None:
    print("Run echo")
    """Echo the user message."""
    text = update.message.text
    print(f"Actions echo:{text}")
    print(f"{update.to_json()}")
    chat_id = update.message.chat_id
    user_name = update.message.from_user.full_name
    # Todo save profile username
    # tele_user_obj = TelegramUser.subscribe(chat_id, user_name)
    # user_recent_searches = tele_user_obj.get_recent_searches(1)
    reply_text = ""
    reply_keyboard = MenuTelegram.REPLY_KEYBOARDS.value.get("default")
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, )
    text = text.replace(CommandsEnum.BACK_BUTTON_PRETEXT, "")
    telegram_service = TelegramService()

    if text in [CommandsEnum.START, '/start']:
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.START
        )
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, )
    elif text == CommandsEnum.HELP:
        reply_text = Message.HELP_TEXT
    elif text == CommandsEnum.TOKEN:
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.TOKEN
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
    print(f"Query callback {query}")
    telegram_service = TelegramService()
    if telegram_service.is_token_address_available(text=query_data):
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.CRYPTO_EXCHANGE, text=query_data
        )
        reply_markup = InlineKeyboardMarkup(reply_keyboard)
        query.edit_message_text(text=f"You have selected {query_data}, {reply_text}", reply_markup=reply_markup)
    elif "_" in query_data:
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.ANALYSIS_CRYPTO_DATA, text=query_data
        )
        reply_markup = InlineKeyboardMarkup(reply_keyboard)
        print(reply_text)
        query.edit_message_text(text=f"{reply_text}", reply_markup=reply_markup)
    else:
        query.answer(text=f"Please select again !")


def run_telegram_bot() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    print("Start run telegram bot")
    updater = Updater(settings.TELEGRAM_BOT_API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(CallbackQueryHandler(callback_echo))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    run_telegram_bot()
