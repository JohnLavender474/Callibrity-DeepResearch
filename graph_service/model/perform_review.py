from pydantic import BaseModel

from model.task import TaskEntry


class PerformReviewInput(BaseModel):
    task_entries: list[TaskEntry]


class PerformReviewOutput(BaseModel):
    review: str
