from datetime import date

from app.infrastructure.db.database import BaseTable

from sqlalchemy import (
    DATE,
    DECIMAL,
    Column,
    ForeignKey,
    Integer,
)


class RideInfo(BaseTable):
    ride_id = Column(
        Integer,
        ForeignKey(
            'rides.ride_id',
            ondelete='CASCADE'
        ),
        primary_key=True
    )
    ride_date = Column(DATE, nullable=False, default=date.today)
    ride_duration = Column(Integer, nullable=False)
    ride_cost = Column(Integer, nullable=False)
    speed_avg = Column(DECIMAL, nullable=False)
    speed_max = Column(DECIMAL, nullable=False)
    stop_times = Column(Integer, nullable=False, default=0)
    distance = Column(DECIMAL, nullable=False)
    refueling = Column(Integer, nullable=False, default=0)
    user_ride_quality = Column(DECIMAL, nullable=False)
    deviation_normal = Column(DECIMAL, nullable=False)

