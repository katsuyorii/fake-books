from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from .dependencies import get_current_user
from .schemas import UserResponseSchema, UserUpdateSchema
from .services import update_user
from .models import UserModel


users_router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@users_router.get('/me', response_model=UserResponseSchema)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@users_router.patch('/me', response_model=UserResponseSchema)
async def update_me(user_update: UserUpdateSchema, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    return await update_user(user_update, current_user, db)