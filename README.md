# Telegram Bot + Google Sheets

This repository contains a ready-to-run Telegram bot that logs incoming messages into a Google Sheet. It uses `python-telegram-bot` for the bot framework and `gspread` for working with Sheets via a service account.

## Features
- `/start` greets the user and explains usage.
- Any text message is stored in the sheet with a timestamp and the sender's name.
- `/list` shows the latest five saved entries.
- `/help` summarizes available commands.

## Getting started
1. Create a Telegram bot with [@BotFather](https://t.me/BotFather) and copy the bot token.
2. Create a Google Cloud service account with Sheets access and generate a JSON key.
3. Share the target spreadsheet with the service account email.
4. Create a worksheet named `bot_entries` (or let the bot create it) with headers `Timestamp`, `User`, and `Message`.

### Environment variables
Place a `.env` file in the project root or set the following variables directly:

```
TELEGRAM_BOT_TOKEN=<bot token>
GOOGLE_SHEETS_ID=<spreadsheet id>
GOOGLE_SERVICE_ACCOUNT_JSON=<full JSON of the service account key>
```

> Tip: For the JSON, you can run `export GOOGLE_SERVICE_ACCOUNT_JSON="$(cat key.json)"`.

### Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the bot
```bash
python main.py
```
The bot will start polling for updates and will create the worksheet if it doesn't exist.

### Project structure
- `main.py`: Application entry point.
- `src/config.py`: Environment-driven settings loader.
- `src/bot.py`: Telegram bot handlers and routing to Sheets.
- `src/google_sheets.py`: Helper wrapper around gspread for interacting with the spreadsheet.
- `requirements.txt`: Project dependencies.

## Development notes
- The bot uses long polling; if you prefer webhooks, wire them in `TelegramSheetBot.run`.
- Avoid committing real tokens or service account keys to version control.
