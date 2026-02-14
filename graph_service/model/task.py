from typing import Optional
from pydantic import BaseModel

from model.citation import Citation


class TaskDecomposition(BaseModel):
    tasks: list[str]


class TaskResult(BaseModel):
    result: str
    reasoning: str
    citations: list[Citation] = []


class TaskEntry(BaseModel):
    task: str
    success: bool
    result: Optional[str] = None
    reasoning: Optional[str] = None
    citations: list[Citation] = []    