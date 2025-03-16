import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from fastapi import HTTPException

from datetime import date


REGEX_NAMES = re.compile(r"^[a-zA-Zа-яА-Я ,.'-]+$")

REGEX_PASSWORD = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = Field(default=None, max_length=256)
    last_name: str | None = Field(default=None, max_length=256)
    date_of_birth: date | None = Field(default=None)
    
    @field_validator('first_name', mode='before')
    @classmethod
    def validate_first_name(cls, value):
        if not REGEX_NAMES.match(value):
            raise HTTPException(
                status_code=422,
                detail="Имя и фамилия могут содержать только буквы, пробелы, апострофы, дефисы и точки."
            )
        return value
    
    @field_validator('last_name', mode='before')
    @classmethod
    def validate_last_name(cls, value):
        if not REGEX_NAMES.match(value):
            raise HTTPException(
                status_code=422,
                detail="Имя и фамилия могут содержать только буквы, пробелы, апострофы, дефисы и точки."
            )
        return value
    
    @field_validator('password', mode='before')
    @classmethod
    def validate_password(cls, value):
        if not REGEX_PASSWORD.match(value):
            raise HTTPException(
                status_code=422,
                detail="Пароль должен содержать минимум 8 символов, хотя бы одну заглавную букву, одну строчную букву, одну цифру и один специальный символ (#?!@$%^&*-)."
            )
        return value
