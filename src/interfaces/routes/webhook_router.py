from fastapi import APIRouter, BackgroundTasks, Request

from config.settings import settings
from src.application.use_cases.process_webhook import ProcessWebhook
from src.infrastructure.sheets.sheets_client import SheetsClient

router = APIRouter()


def _get_use_case() -> ProcessWebhook:
    client = SheetsClient(settings.google_spreadsheet_id)
    return ProcessWebhook(client)


@router.post("/webhook")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    use_case = _get_use_case()
    background_tasks.add_task(use_case.execute, payload)
    return {"status": "ok"}
