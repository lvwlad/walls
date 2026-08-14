import datetime
import hashlib
import os
import uuid

import dotenv
import jwt
from fastapi import Cookie, HTTPException

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def generate_jwt(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def get_hash(password: str, salt: str) -> str:
    hasher = hashlib.sha256()
    hasher.update((password + salt).encode("utf-8"))
    return hasher.hexdigest()


def generate_salt() -> str:
    return str(uuid.uuid4())[12:18]


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def get_current_user_id(session: str | None = Cookie(default=None)) -> int:
    if not session:
        raise HTTPException(
            status_code=401,
            detail={"error": "not_authorized", "message": "Требуется авторизация"},
        )
    try:
        payload = decode_jwt(session)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail={"code": "session_expired", "message": "Сессия истекла, пожалуйста, войдите снова"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail={"error": "not_authorized", "message": "Неверный логин или пароль"},
        )
    return payload["user_id"]
