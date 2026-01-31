from sqlalchemy import Column, String, Float
from datetime import datetime

from model.base import Base


class ProfileModel(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(
        Float,        
        nullable=False,
    )
