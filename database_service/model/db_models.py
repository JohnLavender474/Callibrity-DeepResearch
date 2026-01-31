from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class InvocationModel(Base):
    
    __tablename__ = "invocations"

    invocation_id = Column(
        String,
        primary_key=True,
        index=True,
    )

    profile_id = Column(
        String,
        index=True,
        nullable=False,
    )

    user_query = Column(
        Text,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        default="running",
    )

    graph_state = Column(
        JSON,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
