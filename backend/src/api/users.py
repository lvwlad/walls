from fastapi import APIRouter, Body, Depends
from fastapi.responses import Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_db
from models.models import Profile, User
from schemas.users import CreateUserModel, LoginUserModel
from services.users import generate_jwt, generate_salt, get_current_user_id, get_hash

router = APIRouter(prefix="/api", tags=["users"])


@router.post("/register")
async def create_user(
    user: CreateUserModel,
    response: Response,
    session: Session = Depends(get_db),
):
    if session.query(User).filter(User.email == user.email).first():
        response.status_code = 409
        return {"error": "user_already_exists", "message": "Пользователь с таким email уже зарегистрирован"}

    response.status_code = 201
    salt = generate_salt()
    hash_password = get_hash(user.password, salt)
    new_user = User(
        name=user.name,
        email=user.email,
        salt=salt,
        hash_password=hash_password,
        created_at=session.scalar(func.now()),
    )
    new_user.profile = Profile()
    session.add(new_user)
    session.commit()
    return {"message": "Пользователь зарегистрирован"}


@router.post("/login")
async def login_in_site(
    user_data: LoginUserModel,
    response: Response,
    session: Session = Depends(get_db),
):
    user = (
        session.query(User.id, User.name, User.hash_password, User.salt)
        .filter(User.email == user_data.email)
        .first()
    )
    if not user:
        response.status_code = 401
        return {"error": "invalid_credentials", "message": "Неверный логин или пароль"}

    if get_hash(user_data.password, user.salt) != user.hash_password:
        response.status_code = 401
        return {"error": "invalid_credentials", "message": "Неверный логин или пароль"}

    access_token = generate_jwt(user.id)
    response.set_cookie(key="session", value=access_token, httponly=True, secure=False)
    return {"user_data": {"user_name": user.name}}


@router.get("/me")
async def get_username(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db),
):
    user_name = session.query(User.name).filter(User.id == user_id).first()
    return {"username": user_name.name}


@router.patch("/me/username")
async def rename_me(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db),
    new_name: str = Body(),
):
    user = session.scalar(select(User).where(User.id == user_id))
    user.name = new_name
    session.commit()
    return {"message": "Имя пользователя обновлено"}
