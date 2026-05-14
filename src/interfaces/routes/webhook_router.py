from fastapi import APIRouter, BackgroundTasks, Request

from config.settings import settings
from src.application.use_cases.process_webhook import ProcessWebhook
from src.infrastructure.sheets.sheets_client import SheetsClient
from src.infrastructure.shipstream.shipstream_client import ShipstreamClient

router = APIRouter()


def _get_use_case() -> ProcessWebhook:
    sheets = SheetsClient(settings.google_spreadsheet_id)
    shipstream = ShipstreamClient(settings.buho_api_token)
    return ProcessWebhook(sheets, shipstream)


@router.post("/webhook")
@router.post("/")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    use_case = _get_use_case()
    background_tasks.add_task(use_case.execute, payload)
    return {"status": "ok"}
