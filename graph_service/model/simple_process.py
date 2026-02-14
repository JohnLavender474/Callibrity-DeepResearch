from typing import Optional

from pydantic import BaseModel
from langchain_core.messages import BaseMessage

from model.citation import Citation
from model.execution_config import ExecutionConfig


class SimpleProcessInput(BaseModel):
    query: str
    collection_name: str
    execution_config: ExecutionConfig = ExecutionConfig.default()
    chat_history: Optional[list[BaseMessage]] = None


class SimpleProcessOutput(BaseModel):
    result: str
    citations: list[Citation] = []
