from sqlalchemy import Column, String, Text

from model.base import Base


class DocumentsEmbeddedModel(Base):
    __tablename__ = "documents_embedded"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False, unique=True)
    points = Column(Text, nullable=False)    
