from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey

from model.base import Base


class InvocationModel(Base):
    __tablename__ = "invocations"

    invocation_id = Column(String, primary_key=True)
    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    user_query = Column(String, nullable=False)
    status = Column(String, nullable=False)
    # The graph state is stored as a JSON string in the database.
    # Of course, this is not ideal, but it works for now.
    graph_state = Column(String)
    created_at = Column(
        DateTime,        
        nullable=False,
    )
    updated_at = Column(
        DateTime,        
        nullable=False,
    )