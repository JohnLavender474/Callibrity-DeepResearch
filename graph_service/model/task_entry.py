from pydantic import BaseModel


class TaskDecomposition(BaseModel):
    tasks: list[str]


class TaskEntry(BaseModel):
    task: str
    result: str
    reasoning: str