from app.infrastructure.db.database import BaseTable

from sqlalchemy import (
    DECIMAL,
    Column,
    ForeignKey,
    Integer,
)


class Ride(BaseTable):
    ride_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    driver_id = Column(
        Integer,
        ForeignKey('drivers.driver_id'),
        nullable=False
    )
    car_id = Column(
        Integer,
        ForeignKey('cars.car_id'),
        nullable=False
    )
    rating = Column(DECIMAL, nullable=False, default=10.0)

