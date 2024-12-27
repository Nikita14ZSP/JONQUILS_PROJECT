from app.infrastructure.db.database import async_session
from app.infrastructure.db.models.ride_info import RideInfo
from app.infrastructure.db.models.rides import Ride
from app.repositories.repository import Repository

from sqlalchemy.future import select


class RideRepository(Repository):
    model = Ride


    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            query = (
                select(
                    cls.model,
                    RideInfo
                )
                .join(RideInfo, cls.model.ride_id == RideInfo.ride_id)
                .limit(100)
            )
            result = await session.execute(query)

            return result.fetchall()


    @classmethod
    async def get_by_id(cls, ride_id: int):
        async with async_session() as session:
            query = (
                select(
                    cls.model,
                    RideInfo
                )
                .join(RideInfo, cls.model.ride_id == RideInfo.ride_id)
                .where(cls.model.ride_id == ride_id))
            result = await session.execute(query)

            return result.fetchone()

