from app.infrastructure.db.database import BaseTable

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    Integer,
    String
)


class Car(BaseTable):
    car_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    car_number = Column(String, unique=True, nullable=False)
    is_rented = Column(Boolean, nullable=False, default=False)
    model = Column(String, nullable=False)
    car_type = Column(String, nullable=False)
    fuel_type = Column(String, nullable=False)
    car_rating = Column(DECIMAL, nullable=False, default=10.0)
    year_to_start = Column(Integer, nullable=False)
    year_to_work = Column(Integer, nullable=False)
    rides = Column(Integer, nullable=False, default=0)

