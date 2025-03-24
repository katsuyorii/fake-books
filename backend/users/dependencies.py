from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from auth.utils import verify_access_token
from .services import get_user_by_email
from .models import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)) -> UserModel:
    payload = await verify_access_token(token)
    user = await get_user_by_email(payload.get('sub'), db)

    return user