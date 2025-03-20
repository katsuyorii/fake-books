from fastapi import APIRouter, Depends, Response, Request

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from .schemas import UserRegisterSchema, UserLoginSchema, TokenResponseSchema
from .services import registration, authenticate, logout, refresh


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@auth_router.post('/register', status_code=201)
async def registration_user(user_data: UserRegisterSchema, db: AsyncSession = Depends(get_session)):
    await registration(user_data, db)

    return {'message': 'Пользователь успешно зарегистрирован!'}

@auth_router.post('/login', response_model=TokenResponseSchema)
async def login_user(user: UserLoginSchema, response: Response, db: AsyncSession = Depends(get_session)):
    return await authenticate(user, response, db)

@auth_router.post('/logout')
async def logout_user(response: Response):
    await logout(response)

    return {"message": "Вы вышли из системы"}

@auth_router.post('/refresh', response_model=TokenResponseSchema)
async def refresh_token(request: Request, response: Response):
    return await refresh(request, response)