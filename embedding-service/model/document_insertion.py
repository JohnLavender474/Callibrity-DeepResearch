from typing import Dict

from pydantic import BaseModel


class DocumentInsertion(BaseModel):
    content: str
    metadata: Dict[str, str]
