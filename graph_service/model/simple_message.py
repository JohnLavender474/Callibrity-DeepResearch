from pydantic import BaseModel


class SimpleMessage(BaseModel):
    role: str
    content: str