from fastapi import HTTPException, Response

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import timedelta

from src.config import settings
from users.models import UserModel
from .schemas import UserRegisterSchema, UserLoginSchema, TokenResponseSchema
from .utils import hashing_password, verify_password, create_access_token, create_refresh_token


async def registration(user_data: UserRegisterSchema, db: AsyncSession):
    result = await db.execute(select(UserModel).where(UserModel.email == user_data.email))
    existing_user = result.scalars().one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail='Пользователь с таким email уже существует!'
        )

    user_data_dict = user_data.model_dump()
    user_data_dict['password'] = hashing_password(user_data.password)

    user = UserModel(**user_data_dict)
    db.add(user)
    await db.flush()
    await db.commit()

async def authenticate(user: UserLoginSchema, response: Response, db: AsyncSession) -> TokenResponseSchema:
    result = await db.execute(select(UserModel).where(UserModel.email == user.email))
    existing_user = result.scalars().one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail='Неверный адрес электронный почты или пароль!'
        )
    
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=401,
            detail='Неверный адрес электронный почты или пароль!'
        )
    
    access_token = create_access_token({
        'sub': existing_user.email,
        'role': existing_user.role,
    })

    refresh_token = create_refresh_token({
        'sub': existing_user.email,
        'role': existing_user.role,
    })

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        max_age=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        samesite='Strict',
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        max_age=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        samesite='Strict',
    )

    return TokenResponseSchema(access_token=access_token, token_type='bearer')