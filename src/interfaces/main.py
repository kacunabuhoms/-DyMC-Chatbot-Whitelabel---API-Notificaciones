from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from src.interfaces.routes.webhook_router import router

app = FastAPI(title="API Notificaciones")

app.include_router(router)
