import bcrypt
import jwt

from datetime import datetime, timedelta, timezone

from src.config import settings


def hashing_password(password: str) -> str:
    password_bytes = password.encode()
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password_bytes, salt).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_access_token(payload: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = payload.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({'exp': expire})

    access_token = jwt.encode(payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return access_token

def create_refresh_token(payload: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = payload.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({'exp': expire})

    refresh_token = jwt.encode(payload=to_encode, key=settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)

    return refresh_token