"""Configuration helpers for the Telegram bot project."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotSettings:
    """Settings required to configure the bot and Google Sheets access."""

    telegram_token: str
    spreadsheet_id: str
    service_account_info: dict[str, Any]

    @classmethod
    def from_env(cls) -> "BotSettings":
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_ID")
        service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        if not spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_ID is required")
        if not service_account_json:
            raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON is required")

        try:
            service_account_info = json.loads(service_account_json)
        except json.JSONDecodeError as exc:  # pragma: no cover - sanity guard
            raise ValueError("Invalid GOOGLE_SERVICE_ACCOUNT_JSON value") from exc

        return cls(
            telegram_token=token,
            spreadsheet_id=spreadsheet_id,
            service_account_info=service_account_info,
        )


def get_project_root() -> Path:
    """Return the project root directory."""

    return Path(__file__).resolve().parents[1]
