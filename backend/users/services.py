from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserModel
from .schemas import UserUpdateSchema


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

    