import logging
from typing import Any

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_NAME = "Webhook"


class SheetsClient:
    def __init__(self, spreadsheet_id: str) -> None:
        self._spreadsheet_id = spreadsheet_id
        credentials, _ = google.auth.default(scopes=SCOPES)
        self._service = build("sheets", "v4", credentials=credentials)

    def _sheet(self):
        return self._service.spreadsheets()

    def _get_headers(self) -> list[str]:
        result = (
            self._sheet()
            .values()
            .get(spreadsheetId=self._spreadsheet_id, range=f"{SHEET_NAME}!1:1")
            .execute()
        )
        rows = result.get("values", [[]])
        return rows[0] if rows else []

    def _ensure_headers(self, keys: list[str]) -> list[str]:
        existing = self._get_headers()
        new_keys = [k for k in keys if k not in existing]
        if new_keys:
            updated = existing + new_keys
            self._sheet().values().update(
                spreadsheetId=self._spreadsheet_id,
                range=f"{SHEET_NAME}!1:1",
                valueInputOption="RAW",
                body={"values": [updated]},
            ).execute()
            return updated
        return existing

    async def append_rows(self, rows: list[dict[str, Any]]) -> None:
        if not rows:
            logger.warning("append_rows called with empty rows list")
            return

        logger.info("Appending %d row(s) to sheet '%s'", len(rows), SHEET_NAME)

        all_keys: list[str] = []
        for row in rows:
            for k in row:
                if k not in all_keys:
                    all_keys.append(k)

        logger.info("Keys to write: %s", all_keys)
        headers = self._ensure_headers(all_keys)
        logger.info("Final headers: %s", headers)

        values = [
            [str(row.get(h, "")) if row.get(h) is not None else "" for h in headers]
            for row in rows
        ]

        result = self._sheet().values().append(
            spreadsheetId=self._spreadsheet_id,
            range=f"{SHEET_NAME}!A1",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": values},
        ).execute()
        logger.info("Sheets append result: %s", result)
