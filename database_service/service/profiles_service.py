from typing import Optional

from sqlalchemy.orm import Session

from model.profile import ProfileCreate
from model.profile_model import ProfileModel


def create_profile(
    db: Session,
    profile: ProfileCreate,
) -> ProfileModel:
    db_profile = ProfileModel(
        name=profile.name,
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_profile(
    db: Session,
    profile_id: str,
) -> Optional[ProfileModel]:
    return db.query(ProfileModel).filter(
        ProfileModel.id == profile_id,
    ).first()
