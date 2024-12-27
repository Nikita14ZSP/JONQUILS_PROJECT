from app.infrastructure.db.database import BaseTable
from app.infrastructure.db.models.users import UserSexEnum

from sqlalchemy import (
    DECIMAL,
    Column,
    Enum,
    ForeignKey,
    Integer
)


class Mechanic(BaseTable):
    mechanic_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = Column(
        Integer,
        ForeignKey(
            'users.user_id',
            ondelete='CASCADE'
        ),
        nullable=False
    )
    age = Column(Integer, nullable=False)
    sex = Column(Enum(UserSexEnum, name="user_sex_enum"), nullable=False)
    mechanic_rating = Column(DECIMAL, nullable=False, default=10.0)
    car_times_repaired = Column(Integer, nullable=False, default=0)