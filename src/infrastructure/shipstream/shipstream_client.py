import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_BASE_URL = "https://app.buhologistics.com/api/global/v1"

_PACKAGE_FIELDS = (
    "id",
    "tracking_number",
    "alt_tracking_number",
    "tracking_description",
    "alt_tracking_description",
    "tracking_url",
)
_ADDRESS_FIELDS = ("first_name", "last_name", "telephone", "email")


class ShipstreamClient:
    def __init__(self, token: str) -> None:
        self._token = token

    async def get_order_data(self, order_ref: str) -> dict[str, Any]:
        if not self._token:
            logger.warning("Shipstream API token not configured, skipping enrichment")
            return {"packages": [], "address": {}}

        params = {
            "limit": 100,
            "filter": f"order_ref:{order_ref}",
            "fields:shipments": "all",
            "fields:shipping_address": "all",
            "fields:shipments.packages": "all",
        }
        headers = {"Authorization": f"Bearer {self._token}"}

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{_BASE_URL}/shipping/orders",
                    params=params,
                    headers=headers,
                )
                response.raise_for_status()
                data = response.json()
        except Exception:
            logger.exception("Shipstream API call failed for order_ref=%s", order_ref)
            return {"packages": [], "address": {}}

        included = data.get("included", {})

        raw_packages = included.get("ShipmentPackage", [])
        packages = [
            {f"shipmentpackage.{f}": pkg.get(f) for f in _PACKAGE_FIELDS}
            for pkg in raw_packages
        ]

        raw_addresses = included.get("OrderAddress", [])
        address: dict[str, Any] = {}
        if raw_addresses:
            addr = raw_addresses[0]
            address = {f"orderaddress.{f}": addr.get(f) for f in _ADDRESS_FIELDS}

        logger.info(
            "Shipstream returned %d package(s) for order_ref=%s",
            len(packages),
            order_ref,
        )
        return {"packages": packages, "address": address}
