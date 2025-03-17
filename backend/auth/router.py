from fastapi import APIRouter, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from .schemas import UserRegisterSchema, UserLoginSchema
from .services import registration, authenticate


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@auth_router.post('/register', status_code=201)
async def registration_user(user_data: UserRegisterSchema, db: AsyncSession = Depends(get_session)):
    await registration(user_data, db)

    return {'message': 'Пользователь успешно зарегистрирован!'}

@auth_router.post('/login')
async def login_user(user: UserLoginSchema, response: Response, db: AsyncSession = Depends(get_session)):
    return await authenticate(user, response, db)