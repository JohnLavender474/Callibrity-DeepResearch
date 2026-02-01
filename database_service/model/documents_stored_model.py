from sqlalchemy import Column, DateTime, String

from model.base import Base


class DocumentsStoredModel(Base):
    __tablename__ = "documents_stored"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    profile_id = Column(String, nullable=False)
    uploaded_at = Column(DateTime, nullable=False)
