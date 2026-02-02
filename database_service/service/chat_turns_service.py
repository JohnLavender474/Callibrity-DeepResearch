import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy.orm import Session

from model.chat_turn_model import ChatTurnModel
from model.chat_turn import ChatTurnCreate
from model.conversation_model import ConversationModel


def create_chat_turn(
    db: Session,
    conversation_id: str,
    chat_turn: ChatTurnCreate,
) -> ChatTurnModel:
    id = str(uuid.uuid4())

    db_chat_turn = ChatTurnModel(
        id=id,
        conversation_id=conversation_id,
        role=chat_turn.role,
        data=chat_turn.data,
        timestamp=chat_turn.timestamp,
    )

    db.add(db_chat_turn)

    conversation = db.query(ConversationModel).filter(
        ConversationModel.id == conversation_id
    ).first()

    if conversation:
        conversation.chat_turns = conversation.chat_turns + [id]
        conversation.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_chat_turn)

    return db_chat_turn


def get_chat_turn_by_id(
    db: Session,
    chat_turn_id: str,
) -> Optional[ChatTurnModel]:
    return db.query(ChatTurnModel).filter(
        ChatTurnModel.id == chat_turn_id
    ).first()


def get_chat_turns_by_conversation_id(
    db: Session,
    conversation_id: str,
) -> list[ChatTurnModel] | None:
    return db.query(ChatTurnModel).filter(
        ChatTurnModel.conversation_id == conversation_id
    ).order_by(ChatTurnModel.timestamp.asc()).all()


def update_chat_turn(
    db: Session,
    chat_turn_id: str,
    data: dict[str, Any],
) -> Optional[ChatTurnModel]:
    db_chat_turn = get_chat_turn_by_id(
        db=db,
        chat_turn_id=chat_turn_id,
    )

    if not db_chat_turn:
        return None

    db_chat_turn.data = data

    db.commit()
    db.refresh(db_chat_turn)

    return db_chat_turn


def delete_chat_turn(
    db: Session,
    chat_turn_id: str,
) -> bool:
    db_chat_turn = get_chat_turn_by_id(
        db=db,
        chat_turn_id=chat_turn_id,
    )

    if not db_chat_turn:
        return False

    conversation = db.query(ConversationModel).filter(
        ConversationModel.id == db_chat_turn.conversation_id
    ).first()

    if conversation:
        conversation.chat_turns = [
            turn_id for turn_id in conversation.chat_turns
            if turn_id != chat_turn_id
        ]
        conversation.updated_at = datetime.now(timezone.utc)

    db.delete(db_chat_turn)
    db.commit()

    return True
