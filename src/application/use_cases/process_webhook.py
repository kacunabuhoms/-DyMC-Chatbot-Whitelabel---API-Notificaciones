import json
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any

from src.application.services.flattener import expand_rows, flatten
from src.infrastructure.sheets.sheets_client import SheetsClient
from src.infrastructure.shipstream.shipstream_client import ShipstreamClient

logger = logging.getLogger(__name__)


class ProcessWebhook:
    def __init__(self, sheets_client: SheetsClient, shipstream_client: ShipstreamClient) -> None:
        self._sheets = sheets_client
        self._shipstream = shipstream_client

    async def execute(self, payload: dict[str, Any]) -> None:
        try:
            raw_json = json.dumps(payload, ensure_ascii=False)
            fecha = datetime.now(ZoneInfo("America/Monterrey")).strftime("%Y-%m-%d %H:%M:%S")
            order_ref: str = payload.get("order_ref", "")

            base_row = flatten({k: v for k, v in payload.items() if not isinstance(v, list)})

            shipments_list: list[dict[str, Any]] = payload.get("shipments", [])
            shipments_by_tracking: dict[str, dict[str, Any]] = {
                s["tracking_number"]: flatten(s, "shipments")
                for s in shipments_list
                if "tracking_number" in s
            }

            enrichment = (
                await self._shipstream.get_order_data(order_ref)
                if order_ref
                else {"packages": [], "address": {}}
            )
            packages: list[dict[str, Any]] = enrichment["packages"]
            address: dict[str, Any] = enrichment["address"]

            if packages:
                rows = [
                    {
                        "raw_json": raw_json,
                        "fecha": fecha,
                        **base_row,
                        **shipments_by_tracking.get(pkg.get("shipmentpackage.tracking_number", ""), {}),
                        **address,
                        **pkg,
                    }
                    for pkg in packages
                ]
            else:
                rows = [
                    {"raw_json": raw_json, "fecha": fecha, **row, **address}
                    for row in expand_rows(payload)
                ]

            logger.info("Payload expanded into %d row(s)", len(rows))
            await self._sheets.append_rows(rows)
        except Exception:
            logger.exception("Failed to process webhook payload")
