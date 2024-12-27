from app.infrastructure.db.database import BaseTable
from app.infrastructure.db.models.users import UserSexEnum

from sqlalchemy import (
    DATE,
    DECIMAL,
    Column,
    Enum,
    ForeignKey,
    Integer
)


class Driver(BaseTable):
    driver_id = Column(
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
    driver_rating = Column(DECIMAL, nullable=False, default=10.0)
    driver_rides = Column(Integer, nullable=False, default=0)
    driver_time_accidents = Column(Integer, nullable=False, default=0)
    first_ride_date = Column(DATE, nullable=False)