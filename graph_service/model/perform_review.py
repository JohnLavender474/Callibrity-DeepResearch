from pydantic import BaseModel, Optional

from langchain_core.messages import BaseMessage

from model.task import TaskEntry


class PerformReviewInput(BaseModel):
    task_entries: list[TaskEntry]
    chat_history: Optional[list[BaseMessage]] = None


class PerformReviewOutput(BaseModel):
    review: str
