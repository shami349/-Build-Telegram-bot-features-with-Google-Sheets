"""Telegram bot that syncs with Google Sheets."""
from __future__ import annotations

import logging
from datetime import datetime

from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from .config import BotSettings
from .google_sheets import SheetClient

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

WORKSHEET_NAME = "bot_entries"
HEADERS = ("Timestamp", "User", "Message")


class TelegramSheetBot:
    """Bot wrapper that wires Telegram updates to Google Sheets operations."""

    def __init__(self, settings: BotSettings):
        self.settings = settings
        self.sheet_client = SheetClient(settings.spreadsheet_id, settings.service_account_info)
        self.application = ApplicationBuilder().token(settings.telegram_token).build()

        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("list", self.list_entries))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.log_message))

        self.sheet_client.ensure_worksheet(WORKSHEET_NAME, HEADERS)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a welcome message when the command /start is issued."""

        user = update.effective_user
        if user:
            greeting = f"Hi {user.first_name}! Send me any message to log it to Google Sheets."
        else:  # pragma: no cover - defensive fallback
            greeting = "Hi! Send me any message to log it to Google Sheets."
        await update.message.reply_text(greeting, reply_markup=ForceReply(selective=True))

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Display available bot commands."""

        help_text = (
            "I can log your messages to a Google Sheet.\n"
            "Commands:\n"
            "- /start: Get started.\n"
            "- /list: Show the latest 5 entries from the sheet.\n"
            "- /help: Display this message."
        )
        await update.message.reply_text(help_text)

    async def list_entries(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Return a preview of the latest entries from the sheet."""

        rows = self.sheet_client.get_rows(WORKSHEET_NAME, limit=6)
        if rows and rows[0] == list(HEADERS):
            rows = rows[1:]

        if not rows:
            await update.message.reply_text("No entries yet. Send me a message to log it!")
            return

        preview_lines = ["Latest entries:"]
        for timestamp, user, message in rows[-5:]:
            preview_lines.append(f"• {timestamp} — {user}: {message}")
        await update.message.reply_text("\n".join(preview_lines))

    async def log_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Record user messages to the Google Sheet."""

        user = update.effective_user
        username = user.full_name if user else "Unknown"
        timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        message_text = update.message.text if update.message else ""

        self.sheet_client.append_row(WORKSHEET_NAME, (timestamp, username, message_text))
        await update.message.reply_text("Saved! Use /list to see recent entries.")

    def run(self) -> None:
        logger.info("Starting Telegram bot application")
        self.application.run_polling()
