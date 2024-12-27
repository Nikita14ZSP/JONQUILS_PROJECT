import re

from app.infrastructure.db.models.users import UserRoleEnum

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)


class SUserGet(BaseModel):
    user_id: int
    firstname: str
    lastname: str
    email: EmailStr
    role: UserRoleEnum


class SUserAdd(BaseModel):
    firstname: str = Field(..., min_length=1, max_length=100)
    lastname: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., description='Email address')
    password_hash: str = Field(..., min_length=8, description='Password from 8 symbols')
    role: UserRoleEnum = Field(..., description='User role')


    @classmethod
    @field_validator('firstname')
    def validate_firstname(cls, firstname: str):
        if not firstname.isalpha():
            raise ValueError('Firstname should only contain letters')

        return firstname


    @classmethod
    @field_validator('lastname')
    def validate_lastname(cls, lastname: str):
        if not lastname.isalpha():
            raise ValueError('Lastname should only contain letters')

        return lastname


    @classmethod
    @field_validator('email')
    def validate_email(cls, email: str):
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

        if email and not valid:
            raise ValueError('Email address is not valid')

        return email


class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description='Email address')
    password: str = Field(..., min_length=8, description='Password from 8 symbols')


class SUserUpdate(BaseModel):
    firstname: str | None = Field(None, min_length=1, max_length=100)
    lastname: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = Field(None, description='Email address')

    @classmethod
    @field_validator('firstname')
    def validate_firstname(cls, firstname: str):
        if firstname and not firstname.isalpha():
            raise ValueError('Firstname should only contain letters')

        return firstname

    @classmethod
    @field_validator('lastname')
    def validate_lastname(cls, lastname: str):
        if lastname and not lastname.isalpha():
            raise ValueError('Lastname should only contain letters')

        return lastname

    @classmethod
    @field_validator('email')
    def validate_email(cls, email: str):
        if email:
            valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

            if not valid:
                raise ValueError('Email address is not valid')

        return email