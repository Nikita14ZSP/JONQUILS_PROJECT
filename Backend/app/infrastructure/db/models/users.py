from app.infrastructure.db.database import BaseTable
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    Enum,
    Integer,
    String
)


class UserRoleEnum(PyEnum):
    ADMIN = 'admin'
    DRIVER = 'driver'
    MECHANIC = 'mechanic'


class UserSexEnum(PyEnum):
    MALE = 'male'
    FEMALE = 'female'


class User(BaseTable):
    user_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False, unique=True)
    role = Column(Enum(UserRoleEnum, name="user_role_enum"), nullable=False)

