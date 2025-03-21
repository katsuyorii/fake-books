from fastapi import HTTPException

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from datetime import datetime, date

from auth.schemas import REGEX_PASSWORD
from .models import UserRole


class BaseORMSchema(BaseModel):
    ''' Base schema class for convert to json (ORM) '''
    model_config = ConfigDict(from_attributes=True)

class UserResponseSchema(BaseORMSchema):
    id: int
    email: EmailStr
    role: UserRole
    first_name: str | None
    last_name: str | None
    date_of_birth: date | None
    is_active: bool
    created_at: datetime

class UserUpdateSchema(BaseORMSchema):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None

class UserPasswordUpdateSchema(BaseORMSchema):
    old_password: str
    new_password: str

    @field_validator('new_password', mode='before')
    @classmethod
    def validate_new_password(cls, value):
        if not REGEX_PASSWORD.match(value):
            raise HTTPException(
                status_code=422,
                detail="Пароль должен содержать минимум 8 символов, хотя бы одну заглавную букву, одну строчную букву, одну цифру и один специальный символ (#?!@$%^&*-)."
            )
        return value