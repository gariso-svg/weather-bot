"""
Webhook entry point — use this for server deployment.

Requirements:
  - WEBHOOK_URL must be set in .env (public HTTPS URL of your server)
  - PORT must match the port your reverse proxy exposes (default 8443)
  - Your server must have a valid TLS certificate (Telegram requires HTTPS)

    python webhook_server.py
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
    if not config.WEBHOOK_URL:
        raise RuntimeError(
            "WEBHOOK_URL is not set. "
            "On Railway: go to your service → Variables and add "
            "WEBHOOK_URL=https://<your-app>.up.railway.app"
        )

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

    webhook_url = f"{config.WEBHOOK_URL.rstrip('/')}/webhook"
    logger.info("Bot started in webhook mode. Listening on port %d", config.PORT)
    logger.info("Webhook URL: %s", webhook_url)
    logger.info(
        "Scheduled: beer@%02d:00, morning@09:00, delta@Mon+Thu 09:00 (%s)",
        config.BEER_HOUR,
        config.TIMEZONE,
    )

    app.run_webhook(
        listen="0.0.0.0",
        port=config.PORT,
        url_path="/webhook",
        webhook_url=webhook_url,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
