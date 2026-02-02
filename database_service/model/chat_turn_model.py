from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from model.base import Base


class ChatTurnModel(Base):
    __tablename__ = "chat_turns"

    id = Column(String, primary_key=True)
    conversation_id = Column(
        String,
        ForeignKey("conversations.id"),
        nullable=False,
    )
    role = Column(String, nullable=False)
    data = Column(JSONB, nullable=False)
    timestamp = Column(DateTime, nullable=False)
