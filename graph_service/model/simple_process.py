from typing import Optional

from pydantic import BaseModel
from langchain_core.messages import BaseMessage


class SimpleProcessInput(BaseModel):
    query: str
    messages: Optional[list[BaseMessage]] = None


class SimpleProcessOutput(BaseModel):
    result: str
