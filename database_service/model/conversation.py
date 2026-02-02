from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from model.chat_turn import ChatTurnResponse


class ConversationCreate(BaseModel):    
    profile_id: str
    title: Optional[str] = None
    chat_turns: list[str] = []


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    chat_turns: Optional[list[str]] = None


class ConversationResponse(BaseModel):
    id: str
    profile_id: str
    title: Optional[str] = None
    chat_turns: list[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationWithTurnsResponse(BaseModel):
    id: str
    profile_id: str
    title: Optional[str] = None
    chat_turns: list[ChatTurnResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
