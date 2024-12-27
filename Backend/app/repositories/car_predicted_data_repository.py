from app.infrastructure.db.database import async_session
from app.infrastructure.db.models.cars_predicted_data import CarPredictedData
from app.repositories.repository import Repository

from sqlalchemy.future import select


class CarPredictedDataRepository(Repository):
    model = CarPredictedData

    @classmethod
    async def get_by_id(cls, car_id: int):
        async with async_session() as session:
            query = select(cls.model).where(cls.model.car_id == car_id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

