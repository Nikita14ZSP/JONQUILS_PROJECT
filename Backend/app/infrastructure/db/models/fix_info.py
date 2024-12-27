from datetime import datetime

from app.infrastructure.db.database import BaseTable

from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String
)


class FixInfo(BaseTable):
    fix_info_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    car_id = Column(
        Integer,
        ForeignKey('cars.car_id'),
        nullable=False
    )
    mechanic_id = Column(
        Integer,
        ForeignKey('mechanics.mechanic_id'),
        nullable=False
    )
    fix_date = Column(TIMESTAMP, nullable=False, default=datetime.now())
    work_type = Column(String, nullable=False)
    destroy_degree = Column(DECIMAL, nullable=False)
    work_duration = Column(Integer, nullable=False)
