from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_spreadsheet_id: str
    app_env: str = "development"

    # Fase 2
    meta_token: str = ""
    meta_phone_number_id: str = ""
    meta_verify_token: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
