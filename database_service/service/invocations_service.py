import json
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from model.invocation_model import InvocationModel
from model.invocation import (
    InvocationCreate,
    InvocationUpdate,
)


def create_invocation(
    db: Session,
    profile_id: str,
    invocation: InvocationCreate,
) -> InvocationModel:
    now = datetime.now(timezone.utc)
    graph_state_str = None
    if invocation.graph_state is not None:
        graph_state_str = json.dumps(invocation.graph_state)

    db_invocation = InvocationModel(
        invocation_id=invocation.invocation_id,
        profile_id=profile_id,
        user_query=invocation.user_query,
        status=invocation.status,
        graph_state=graph_state_str,
        created_at=now,
        updated_at=now,
    )

    db.add(db_invocation)
    db.commit()
    db.refresh(db_invocation)
    
    return db_invocation


def get_invocation_by_id(
    db: Session,
    invocation_id: str,
    profile_id: str,
) -> Optional[InvocationModel]:
    return db.query(InvocationModel).filter(
        InvocationModel.invocation_id == invocation_id,
        InvocationModel.profile_id == profile_id,
    ).first()


def get_invocations_by_profile_id(
    db: Session,
    profile_id: str,    
    limit: Optional[int] = None,
) -> list[InvocationModel]:
    query = db.query(InvocationModel).filter(
        InvocationModel.profile_id == profile_id
    ).order_by(
        InvocationModel.created_at.desc()
    )
    
    if limit is not None:
        query = query.limit(limit)

    return query.all()


def update_invocation(
    db: Session,
    invocation_id: str,
    invocation_update: InvocationUpdate,
    profile_id: str,
) -> Optional[InvocationModel]:
    db_invocation = get_invocation_by_id(
        db=db,
        invocation_id=invocation_id,
        profile_id=profile_id,
    )
    
    if not db_invocation:
        return None
    
    if invocation_update.status is not None:
        db_invocation.status = invocation_update.status
    
    if invocation_update.graph_state is not None:
        db_invocation.graph_state = json.dumps(
            invocation_update.graph_state
        )
    
    db_invocation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_invocation)
    return db_invocation


def delete_invocation_by_id(
    db: Session,
    invocation_id: str,
    profile_id: str,
) -> bool:
    db_invocation = get_invocation_by_id(
        db=db,
        invocation_id=invocation_id,
        profile_id=profile_id,
    )
    
    if not db_invocation:
        return False
    
    db.delete(db_invocation)
    db.commit()
    return True
