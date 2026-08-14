from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models.models import Profile, User
from schemas.profiles import ProfileData
from services.users import get_current_user_id

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("/{username}", response_model=ProfileData)
async def get_profile_data(
    username: str = Path(),
    session: Session = Depends(get_db),
):
    profile = session.scalar(
        select(Profile).join(User).where(User.name == username)
    )
    if not profile:
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "message": f"Профиль {username} не найден"},
        )
    return profile


@router.patch("/me/bio")
async def change_bio(
    session: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    new_bio: str = Body(max_length=567),
):
    profile = session.scalar(select(Profile).where(Profile.user_id == user_id))
    profile.bio = new_bio
    session.commit()
    return {"message": "Bio updated", "profile": profile}


@router.patch("/me/quote")
async def change_quote(
    session: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    new_quote: str = Body(max_length=150),
):
    profile = session.scalar(select(Profile).where(Profile.user_id == user_id))
    profile.quote = new_quote
    session.commit()
    session.refresh(profile)
    return {
        "message": "Quote updated",
        "profile": ProfileData.model_validate(profile).model_dump(),
    }


@router.patch("/me/avatar")
async def change_avatar(
    session: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    avatar_link: str = Body(),
):
    profile = session.scalar(select(Profile).where(Profile.user_id == user_id))
    profile.avatar = avatar_link
    session.commit()
    session.refresh(profile)
    return {
        "message": "Avatar updated",
        "profile": ProfileData.model_validate(profile).model_dump(),
    }


@router.patch("/me/banner")
async def change_banner(
    session: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    banner_link: str = Body(),
):
    profile = session.scalar(select(Profile).where(Profile.user_id == user_id))
    profile.banner = banner_link
    session.commit()
    session.refresh(profile)
    return {
        "message": "Banner updated",
        "profile": ProfileData.model_validate(profile).model_dump(),
    }
