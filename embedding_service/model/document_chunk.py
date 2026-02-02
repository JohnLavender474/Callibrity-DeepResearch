from pydantic import BaseModel


class DocumentChunk(BaseModel):
    page_number: int
    text: str
