from typing import Optional

from pydantic import BaseModel
from langchain_core.messages import BaseMessage


class SimpleProcessInput(BaseModel):
    query: str
    chat_history: Optional[list[BaseMessage]] = None


class SimpleProcessOutput(BaseModel):
    result: str
