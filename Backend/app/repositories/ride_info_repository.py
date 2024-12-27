from app.infrastructure.db.database import async_session
from app.infrastructure.db.models.ride_info import RideInfo
from app.repositories.repository import Repository

from sqlalchemy.future import select


class RideInfoRepository(Repository):
    model = RideInfo

    @classmethod
    async def get_by_id(cls, ride_id: int):
        async with async_session() as session:
            query = select(cls.model).where(cls.model.ride_id == ride_id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

