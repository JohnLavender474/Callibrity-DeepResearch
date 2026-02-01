from pydantic import BaseModel


class DocumentsEmbeddedCreate(BaseModel):
    filename: str
    points: str


class DocumentsEmbeddedResponse(BaseModel):
    id: str
    filename: str
    points: str

    class Config:
        from_attributes = True
