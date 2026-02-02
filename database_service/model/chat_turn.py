from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ChatTurnCreate(BaseModel):
    role: str
    data: dict[str, Any]
    timestamp: datetime


class ChatTurnResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    data: dict[str, Any]
    timestamp: datetime

    class Config:
        from_attributes = True
