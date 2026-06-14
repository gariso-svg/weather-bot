"""
Polling entry point — run this for local development.

    python bot.py
"""

import datetime
import logging
import zoneinfo

from telegram.ext import ApplicationBuilder, CommandHandler

import config
from handlers import (
    handle_error,
    handle_start,
    handle_weather,
    send_beer_notification,
    send_delta_reminder,
    send_morning_reminder,
)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("weather", handle_weather))
    app.add_error_handler(handle_error)

    tz = zoneinfo.ZoneInfo(config.TIMEZONE)
    app.job_queue.run_daily(
        send_beer_notification,
        time=datetime.time(hour=config.BEER_HOUR, minute=0, tzinfo=tz),
    )
    app.job_queue.run_daily(
        send_morning_reminder,
        time=datetime.time(hour=9, minute=0, tzinfo=tz),
    )
    app.job_queue.run_daily(
        send_delta_reminder,
        time=datetime.time(hour=9, minute=0, tzinfo=tz),
        days=(0, 3),
    )

    logger.info(
        "Bot started in polling mode. Scheduled: beer@%02d:00, morning@09:00, delta@Mon+Thu 09:00 (%s). Press Ctrl+C to stop.",
        config.BEER_HOUR,
        config.TIMEZONE,
    )
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
