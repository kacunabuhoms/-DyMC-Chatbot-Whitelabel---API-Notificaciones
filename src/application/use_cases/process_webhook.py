import json
import logging
from typing import Any

from src.application.services.flattener import expand_rows
from src.infrastructure.sheets.sheets_client import SheetsClient

logger = logging.getLogger(__name__)


class ProcessWebhook:
    def __init__(self, sheets_client: SheetsClient) -> None:
        self._sheets = sheets_client

    async def execute(self, payload: dict[str, Any]) -> None:
        try:
            raw_json = json.dumps(payload, ensure_ascii=False)
            rows = [{"raw_json": raw_json, **row} for row in expand_rows(payload)]
            logger.info("Payload expanded into %d row(s)", len(rows))
            await self._sheets.append_rows(rows)
        except Exception:
            logger.exception("Failed to process webhook payload")
