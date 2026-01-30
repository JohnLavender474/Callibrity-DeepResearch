from pydantic import BaseModel

from model.task import TaskEntry


class PerformResearchInput(BaseModel):
    query: str
    collection_name: str


class PerformResearchOutput(BaseModel):
    task_entries: list[TaskEntry]
