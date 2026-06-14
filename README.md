# Telegram Weather Bot

A Python Telegram bot that returns current weather for any city using the OpenWeatherMap API.  
Supports **polling mode** (local development) and **webhook mode** (server deployment).

---

## Prerequisites

- Python 3.11 or newer
- `pip` (comes with Python)
- A Telegram account
- A free Weatherbit account

---

## Step 1 — Get a Telegram Bot Token

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot` and follow the prompts:
   - Choose a display name (e.g. `My Weather Bot`)
   - Choose a username ending in `bot` (e.g. `myweather_bot`)
3. BotFather will reply with your **token** — a string like `1234567890:ABCdef...`  
   Keep it secret; anyone with it can control your bot.

---

## Step 2 — Get a Weatherbit API Key

1. Go to <https://www.weatherbit.io/account/create> and create a free account.
2. Open the **API Keys** section in your account dashboard.
3. Copy the default key (or create a new one).  
   Free tier includes 50 calls/day to the current weather endpoint.

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Configure Environment Variables

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in your values:

```env
BOT_TOKEN=1234567890:ABCdef...
WEATHERBIT_API_KEY=your_weatherbit_key_here
```

> **Important:** Never commit `.env` to version control. It is already listed in `.gitignore`.

---

## Step 5 — Run Locally (Polling Mode)

```bash
python bot.py
```

The bot starts polling Telegram for new messages.  
Open your bot in Telegram and send:

- `/start` — welcome message
- `/weather London` — current weather for London
- `/weather New York` — works with multi-word city names too

Press **Ctrl+C** to stop.

---

## Step 6 — Deploy to a Server (Webhook Mode)

Webhook mode requires a public server with a valid HTTPS certificate.

### 6a. Set the webhook variables in `.env`

```env
WEBHOOK_URL=https://yourdomain.com
PORT=8443
```

Telegram accepts webhooks on ports **443**, **80**, **88**, and **8443**.

### 6b. Start the webhook server

```bash
python webhook_server.py
```

The server listens on `0.0.0.0:<PORT>` and registers `<WEBHOOK_URL>/webhook` with Telegram automatically.

### 6c. Reverse proxy (recommended)

Run the bot behind **nginx** or **Caddy** so TLS termination is handled by the proxy:

```
[Telegram] → HTTPS → [nginx :443] → HTTP → [webhook_server.py :8443]
```

Minimal nginx location block:

```nginx
location /webhook {
    proxy_pass http://127.0.0.1:8443/webhook;
    proxy_set_header Host $host;
}
```

### 6d. Process manager (optional)

Keep the bot running after logout with **systemd** or **supervisor**:

```bash
# systemd example
[Unit]
Description=Telegram Weather Bot
After=network.target

[Service]
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 webhook_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Project Structure

```
c:\bot\
├── bot.py              # Polling entry point (local dev)
├── webhook_server.py   # Webhook entry point (server deploy)
├── config.py           # Loads .env variables, validates required keys
├── weather.py          # OpenWeatherMap client + response formatter
├── handlers.py         # Telegram command handlers
├── requirements.txt    # Python dependencies
├── .env.example        # Template — copy to .env and fill in secrets
└── .cursor\
    ├── agents\         # Cursor subagents for bot & weather development
    ├── rules\          # Coding standards enforced by Cursor AI
    └── hooks.json      # Automation hooks (secret-leak detection, etc.)
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message with usage instructions |
| `/weather <city>` | Current weather for the specified city |

---

## Troubleshooting

| Problem | Solution |
|---------|---------|
| `RuntimeError: BOT_TOKEN is not set` | Make sure `.env` exists and `BOT_TOKEN` is filled in |
| `RuntimeError: WEATHERBIT_API_KEY is not set` | Make sure `WEATHERBIT_API_KEY` is filled in in `.env` |
| City not found | Check the city spelling; try adding the country code: `/weather Paris,FR` |
| `RuntimeError: WEBHOOK_URL is not set` | Set `WEBHOOK_URL` in `.env` before running `webhook_server.py` |
| Bot doesn't respond in webhook mode | Verify your server is publicly reachable and TLS certificate is valid |

---

## License

MIT
