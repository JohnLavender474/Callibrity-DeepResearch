from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from model.chat_turn import (
    ChatTurnCreate,
    ChatTurnResponse,
)
from service import chat_turns_service
from service import conversations_service
from dependencies import get_db

import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/database",
    tags=["database"],
)


@router.post(
    "/{profile_id}/conversations/{conversation_id}/chat-turns",
    response_model=ChatTurnResponse,
)
def create_chat_turn(
    profile_id: str,
    conversation_id: str,
    chat_turn: ChatTurnCreate,
    db: Session = Depends(get_db),
):
    conversation = conversations_service.get_conversation_by_id(
        db=db,
        conversation_id=conversation_id,
        profile_id=profile_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    logger.info(
        f"Creating chat turn for conversation {conversation_id} "
        f"in profile {profile_id}"
    )

    return chat_turns_service.create_chat_turn(
        db=db,
        conversation_id=conversation_id,
        chat_turn=chat_turn,
    )


@router.get(
    "/{profile_id}/conversations/{conversation_id}/chat-turns",
    response_model=list[ChatTurnResponse],
)
def get_chat_turns(
    profile_id: str,
    conversation_id: str,
    db: Session = Depends(get_db),
):
    conversation = conversations_service.get_conversation_by_id(
        db=db,
        conversation_id=conversation_id,
        profile_id=profile_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    logger.info(
        f"Fetching chat turns for conversation {conversation_id} "
        f"in profile {profile_id}"
    )

    return chat_turns_service.get_chat_turns_by_conversation_id(
        db=db,
        conversation_id=conversation_id,
    )


@router.get(
    "/{profile_id}/chat-turns/{chat_turn_id}",
    response_model=ChatTurnResponse,
)
def get_chat_turn(
    profile_id: str,
    chat_turn_id: str,
    db: Session = Depends(get_db),
):
    chat_turn = chat_turns_service.get_chat_turn_by_id(
        db=db,
        chat_turn_id=chat_turn_id,
    )

    if not chat_turn:
        raise HTTPException(
            status_code=404,
            detail="Chat turn not found",
        )

    conversation = conversations_service.get_conversation_by_id(
        db=db,
        conversation_id=chat_turn.conversation_id,
        profile_id=profile_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found or does not belong to profile",
        )

    return chat_turn


@router.patch(
    "/{profile_id}/chat-turns/{chat_turn_id}",
    response_model=ChatTurnResponse,
)
def update_chat_turn(
    profile_id: str,
    chat_turn_id: str,
    data: dict[str, Any],
    db: Session = Depends(get_db),
):
    chat_turn = chat_turns_service.get_chat_turn_by_id(
        db=db,
        chat_turn_id=chat_turn_id,
    )

    if not chat_turn:
        raise HTTPException(
            status_code=404,
            detail="Chat turn not found",
        )

    conversation = conversations_service.get_conversation_by_id(
        db=db,
        conversation_id=chat_turn.conversation_id,
        profile_id=profile_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found or does not belong to profile",
        )

    logger.info(
        f"Updating chat turn {chat_turn_id} in profile {profile_id}"
    )

    updated = chat_turns_service.update_chat_turn(
        db=db,
        chat_turn_id=chat_turn_id,
        data=data,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Chat turn not found",
        )

    return updated


@router.delete(
    "/{profile_id}/chat-turns/{chat_turn_id}",
)
def delete_chat_turn(
    profile_id: str,
    chat_turn_id: str,
    db: Session = Depends(get_db),
):
    chat_turn = chat_turns_service.get_chat_turn_by_id(
        db=db,
        chat_turn_id=chat_turn_id,
    )

    if not chat_turn:
        raise HTTPException(
            status_code=404,
            detail="Chat turn not found",
        )

    conversation = conversations_service.get_conversation_by_id(
        db=db,
        conversation_id=chat_turn.conversation_id,
        profile_id=profile_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found or does not belong to profile",
        )

    logger.info(
        f"Deleting chat turn {chat_turn_id} in profile {profile_id}"
    )

    deleted = chat_turns_service.delete_chat_turn(
        db=db,
        chat_turn_id=chat_turn_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Chat turn not found",
        )

    return {"message": "Chat turn deleted successfully"}
