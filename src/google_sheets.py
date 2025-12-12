"""Google Sheets helper utilities."""
from __future__ import annotations

from typing import Iterable, List, Sequence

import gspread
from google.oauth2.service_account import Credentials


class SheetClient:
    """A minimal wrapper around gspread to simplify bot interactions."""

    def __init__(self, spreadsheet_id: str, service_account_info: dict):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        self._client = gspread.authorize(credentials)
        self._spreadsheet = self._client.open_by_key(spreadsheet_id)

    def append_row(self, worksheet_name: str, values: Sequence[str]) -> None:
        worksheet = self._spreadsheet.worksheet(worksheet_name)
        worksheet.append_row(list(values), value_input_option="USER_ENTERED")

    def get_rows(self, worksheet_name: str, limit: int | None = None) -> List[List[str]]:
        worksheet = self._spreadsheet.worksheet(worksheet_name)
        rows: List[List[str]] = worksheet.get_all_values()
        if limit is None:
            return rows
        return rows[:limit]

    def ensure_worksheet(self, worksheet_name: str, headers: Iterable[str]) -> None:
        """Ensure the worksheet exists and has the expected headers."""

        try:
            worksheet = self._spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            self._spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=len(list(headers)))
            worksheet = self._spreadsheet.worksheet(worksheet_name)
            worksheet.append_row(list(headers))
            return

        existing_headers = worksheet.row_values(1)
        if existing_headers != list(headers):
            worksheet.update("A1", [list(headers)])
