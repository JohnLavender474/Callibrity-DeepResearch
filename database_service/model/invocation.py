import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class InvocationCreate(BaseModel):
    invocation_id: str
    profile_id: str
    user_query: str
    status: str = "running"
    graph_state: Optional[dict] = None


class InvocationUpdate(BaseModel):
    status: Optional[str] = None
    graph_state: Optional[dict] = None


class InvocationResponse(BaseModel):
    invocation_id: str
    profile_id: str
    user_query: str
    status: str
    graph_state: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_validator("graph_state", mode="before")
    @classmethod
    def parse_graph_state(cls, value: str | dict | None) -> (
        dict | None
    ):
        if value is None:
            return None
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            return json.loads(value)
        return value
