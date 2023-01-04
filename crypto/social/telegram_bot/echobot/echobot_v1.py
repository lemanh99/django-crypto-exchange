import logging

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from telegram import Update, ForceReply, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
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


def remove_chat_buttons(bot, chat_id: int, text: str):
    """Deletes buttons below the chat.
    For now there are no way to delete kbd other than inline one, check
        https://core.telegram.org/bots/api#updating-messages.
    """
    bot.send_message(chat_id, text=text, reply_markup=ReplyKeyboardRemove())


def echo(update: Update, _: CallbackContext) -> None:
    print("Run echo")
    """Echo the user message."""
    text = update.message.text
    print(f"Actions echo:{text}")
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
    elif text in [CommandsEnum.TOKEN, '/token']:
        remove_chat_buttons(bot=update.message.bot, chat_id=update.message.chat_id, text="Hi !!")
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.TOKEN
        )
        reply_markup = InlineKeyboardMarkup(reply_keyboard)
    elif text == CommandsEnum.CANCEL:
        remove_chat_buttons(update.message.bot, update.message.chat_id, text=Message.GOODBYE)
    else:
        reply_text = Message.UNKNOWN_COMMAND.format(text=text)

    update.message.reply_text(
        reply_text,
        reply_markup=reply_markup
    )


def callback_echo(update, context):
    query = update.callback_query
    query_data = query.data
    print("callback_echo", query_data)
    print("Debug: Data callback", query)
    chat_id = query.message.chat.id
    telegram_service = TelegramService()
    if telegram_service.is_token_address_available(text=query_data):
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.CRYPTO_EXCHANGE, text=query_data
        )
        reply_markup = InlineKeyboardMarkup(reply_keyboard)
        query.edit_message_text(text=f"You have selected {query_data}, {reply_text}", reply_markup=reply_markup)
    elif "_" in query_data and query_data.count('_') == 1:
        reply_text, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.TIME_EXCHANGE, text=query_data
        )
        reply_markup = InlineKeyboardMarkup(reply_keyboard)
        query.edit_message_text(text=f"You have selected {query_data.replace('_', '-')}, {reply_text}",
                                reply_markup=reply_markup)
    elif "_" in query_data and query_data.count('_') == 2:
        query.edit_message_text(text=f"You select exchange {query_data.replace('_', '-')}", parse_mode='HTML')
        data_analysis, reply_keyboard = telegram_service.get_message_and_keyboards_by_text_command(
            text_command=CommandsEnum.ANALYSIS_CRYPTO_DATA, text=query_data
        )
        template = get_template("telegram/information_analysis_data.html")
        for data in data_analysis:
            render_context = Context(dict(**data))
            html = template.template.render(render_context)
            context.bot.send_message(chat_id=chat_id, text=str(html), parse_mode='HTML')
    else:
        query.answer(text=f"Please select again !")


def run_telegram_bot_v1() -> None:
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
