import logging

from telegram import Update
from telegram.ext import ContextTypes

from beer import format_beer_message, get_random_beer
from storage import load_chat_ids, save_chat_id
from weather import format_weather, get_weather

logger = logging.getLogger(__name__)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    save_chat_id(update.effective_chat.id)
    await update.message.reply_text(
        "Hello! I can show you the current weather anywhere in the world.\n\n"
        "Send /weather <city> to get started.\n"
        "Example: /weather London"
    )


async def send_beer_notification(context: ContextTypes.DEFAULT_TYPE) -> None:
    beer = get_random_beer()
    text = format_beer_message(beer)
    for chat_id in load_chat_ids():
        try:
            await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
        except Exception:
            logger.warning("Could not send beer notification to chat_id=%s", chat_id, exc_info=True)


async def send_morning_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Доброе утро! ☀️\n\n"
        "Не забудь включить свои счета, а также проверь СПК и наличие выплат и их СЛА."
    )
    for chat_id in load_chat_ids():
        try:
            await context.bot.send_message(chat_id=chat_id, text=text)
        except Exception:
            logger.warning("Could not send morning reminder to chat_id=%s", chat_id, exc_info=True)


async def send_delta_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Привет! Напоминаю: сегодня нужно собрать дельту. Не откладывай на потом!"
    for chat_id in load_chat_ids():
        try:
            await context.bot.send_message(chat_id=chat_id, text=text)
        except Exception:
            logger.warning("Could not send delta reminder to chat_id=%s", chat_id, exc_info=True)


async def handle_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text(
            "Please provide a city name after the command.\n"
            "Example: /weather Berlin"
        )
        return

    city = " ".join(args)
    await update.message.reply_text(f"Fetching weather for {city}...")

    data, error = await get_weather(city)
    if error:
        await update.message.reply_text(error)
        return

    await update.message.reply_text(format_weather(data))


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Unhandled exception while processing update: %s", context.error, exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "An unexpected error occurred. Please try again later."
        )
