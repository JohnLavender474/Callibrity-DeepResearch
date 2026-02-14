from pydantic import BaseModel


class Citation(BaseModel):
    filename: str
    content_summary: str
    page_number: int
    chunk_index: int
    collection_name: str
    score: float
    content: str