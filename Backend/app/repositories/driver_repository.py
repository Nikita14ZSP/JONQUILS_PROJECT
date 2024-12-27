from app.infrastructure.db.database import async_session
from app.infrastructure.db.models.drivers import Driver
from app.infrastructure.db.models.rides import Ride
from app.infrastructure.db.models.ride_info import RideInfo
from app.infrastructure.db.models.users import User
from app.repositories.repository import Repository

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError


class DriverRepository(Repository):
    model = Driver


    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            query = (
                select(
                    cls.model,
                    User
                )
                .join(User, User.user_id == cls.model.user_id)
                .limit(100)
            )
            result = await session.execute(query)

            return result.fetchall()


    @classmethod
    async def get_by_user_id(cls, user_id: int):
        async with async_session() as session:
            query = (
                select(
                    cls.model,
                    User
                )
                .join(User, User.user_id == cls.model.user_id)
                .where(cls.model.user_id == user_id)
            )
            result = await session.execute(query)

            return result.fetchone()


    @classmethod
    async def get_by_driver_id(cls, driver_id: int):
        async with async_session() as session:
            query = (
                select(
                    cls.model,
                    User
                )
                .join(User, User.user_id == cls.model.user_id)
                .where(cls.model.driver_id == driver_id)
            )
            result = await session.execute(query)

            return result.fetchone()


    @classmethod
    async def get_driver_rides(cls, driver_id: int):
        async with async_session() as session:
            try:
                query = (
                    select(
                        cls.model.driver_id,
                        Ride,
                        RideInfo
                    )
                    .join(Ride, Ride.driver_id == Driver.driver_id)
                    .join(RideInfo, Ride.ride_id == RideInfo.ride_id)
                    .where(cls.model.driver_id == driver_id)
                )
                result = await session.execute(query)

                return result.fetchall()
            except SQLAlchemyError as error:
                raise error

