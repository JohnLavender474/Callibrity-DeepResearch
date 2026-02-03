from typing import Optional, Any

from pydantic import BaseModel


class SearchResultMetadata(BaseModel):
    source_name: str
    content: str
    page_number: Optional[int] = None
    chunk_index: Optional[int] = None
    custom_metadata: dict[str, Any] = {}


class SearchResult(BaseModel):
    id: str
    score: float   
    metadata: SearchResultMetadata

    # The content summary should be filled in 
    # by the caller based on their own logic.
    # It is blank by default.    
    content_summary: str = ""
