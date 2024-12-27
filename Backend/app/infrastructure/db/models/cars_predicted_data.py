from app.infrastructure.db.database import BaseTable

from sqlalchemy import (
    DECIMAL,
    Column,
    ForeignKey,
    Integer,
    String
)


class CarPredictedData(BaseTable):
    car_id = Column(
        Integer,
        ForeignKey(
            'cars.car_id',
            ondelete='CASCADE'
        ),
        primary_key=True
    )
    target_reg = Column(DECIMAL, nullable=False)
    target_class = Column(String, nullable=False)

