from pydantic import BaseModel

from model.simple_message import SimpleMessage


class GraphInput(BaseModel):
    user_query: str
    profile_id: str
    messages: list[SimpleMessage] = []