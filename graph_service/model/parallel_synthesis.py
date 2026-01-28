from typing import Optional

from pydantic import BaseModel
from langchain_core.messages import BaseMessage

from graph_service.model.task_entry import TaskEntry


class ParallelSynthesisInput(BaseModel):
    query: str
    collection_name: str
    messages: Optional[list[BaseMessage]] = None


class ParallelSynthesisOutput(BaseModel):
    overall_result: str
    task_entries: list[TaskEntry]
