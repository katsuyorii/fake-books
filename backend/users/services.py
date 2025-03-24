from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hashing_password, verify_password
from .models import UserModel
from .schemas import UserUpdateSchema, UserPasswordUpdateSchema


async def get_user_by_email(email: str, db: AsyncSession) -> UserModel | None:
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    return result.scalars().one_or_none()

async def update_user(user_update: UserUpdateSchema, current_user: UserModel, db: AsyncSession) -> UserModel:
    update_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    db.add(current_user)
    await db.flush()
    await db.commit()
    await db.refresh(current_user)

    return current_user

async def update_password_user(user_passwords: UserPasswordUpdateSchema, current_user: UserModel, db: AsyncSession):
    user_passwords_data = user_passwords.model_dump()

    if not await verify_password(user_passwords_data.get('old_password'), current_user.password):
        raise HTTPException(
            status_code=401,
            detail='Текущий пароль введен не верно!'
        )
    
    current_user.password = await hashing_password(user_passwords_data.get('new_password'))

    db.add(current_user)
    await db.flush()
    await db.commit()
