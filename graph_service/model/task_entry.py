from pydantic import BaseModel


class TaskEntry(BaseModel):
    task: str
    result: str
    reasoning: str