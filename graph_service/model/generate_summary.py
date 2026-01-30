from pydantic import BaseModel

from model.task import TaskEntry


class GenerateSummaryInput(BaseModel):
    task_entries: list[TaskEntry]
    review: str


class GenerateSummaryOutput(BaseModel):
    summary: str
