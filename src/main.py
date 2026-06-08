import json
import logging

from dotenv import load_dotenv
load_dotenv()

from fastapi import BackgroundTasks, FastAPI, Request

from config.settings import settings
from src.sheets import append_raw

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API Notificaciones")


@app.post("/webhook")
@app.post("/")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    raw_json = json.dumps(payload, ensure_ascii=False)
    background_tasks.add_task(append_raw, settings.google_spreadsheet_id, raw_json)
    return {"status": "ok"}
