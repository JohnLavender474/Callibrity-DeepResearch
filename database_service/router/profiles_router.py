from fastapi import (
    APIRouter,
    Depends,    
)
from sqlalchemy.orm import Session

from model.profile import ProfileCreate, ProfileResponse
from service import profiles_service
from dependencies import get_db

import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/database",
    tags=["database"],
)


@router.post(
    "/profiles",
    response_model=ProfileResponse,
)
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
):
    logger.info(f"Creating profile: {profile.name}")

    created = profiles_service.create_profile(
        db=db,
        profile=profile,
    )

    return created



