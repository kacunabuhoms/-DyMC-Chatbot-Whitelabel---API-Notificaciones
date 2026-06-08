import asyncio
import logging

import google.auth
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_NAME = "E1 - Raw json"


def _append(spreadsheet_id: str, raw_json: str) -> None:
    credentials, _ = google.auth.default(scopes=SCOPES)
    service = build("sheets", "v4", credentials=credentials)
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=f"{SHEET_NAME}!A:A",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [[raw_json]]},
        )
        .execute()
    )
    logger.info("Sheets append result: %s", result)


async def append_raw(spreadsheet_id: str, raw_json: str) -> None:
    await asyncio.to_thread(_append, spreadsheet_id, raw_json)
