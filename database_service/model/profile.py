from pydantic import BaseModel


class ProfileCreate(BaseModel):
    name: str


class ProfileResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True
