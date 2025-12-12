"""Entry point for running the Telegram bot."""
from __future__ import annotations

from src.bot import TelegramSheetBot
from src.config import BotSettings


def main() -> None:
    settings = BotSettings.from_env()
    bot = TelegramSheetBot(settings)
    bot.run()


if __name__ == "__main__":
    main()
