from typing import Any

from pydantic import BaseModel


class WebhookPayload(BaseModel):
    model_config = {"extra": "allow"}

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()
