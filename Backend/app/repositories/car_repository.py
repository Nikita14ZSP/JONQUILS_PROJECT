from app.infrastructure.db.database import async_session
from app.infrastructure.db.models.cars import Car
from app.infrastructure.db.models.fix_info import FixInfo
from app.infrastructure.db.models.mechanics import Mechanic
from app.infrastructure.db.models.rides import Ride
from app.infrastructure.db.models.ride_info import RideInfo
from app.infrastructure.db.models.cars_predicted_data import CarPredictedData
from app.repositories.repository import Repository

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError


class CarRepository(Repository):
    model = Car


    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            query = (
                select(
                    cls.model,
                )
                .limit(100)
            )
            result = await session.execute(query)

            return result.fetchall()


    @classmethod
    async def get_all_with_predict(cls):
        async with async_session() as session:
            query = (
                select(
                    cls.model,
                    CarPredictedData
                )
                .join(CarPredictedData, CarPredictedData.car_id == cls.model.car_id)
            )
            result = await session.execute(query)

            return result.fetchall()


    @classmethod
    async def get_by_id(cls, car_id: int):
        async with async_session() as session:
            query = (
                select(
                    cls.model
                )
                .where(cls.model.car_id == car_id)
            )
            result = await session.execute(query)

            return result.fetchone()


    @classmethod
    async def get_by_id_with_predict(cls, car_id: int):
        async with async_session() as session:
            query = (
                select(
                    cls.model,
                    CarPredictedData
                )
                .join(CarPredictedData, CarPredictedData.car_id == cls.model.car_id)
                .where(cls.model.car_id == car_id)
            )
            result = await session.execute(query)

            return result.fetchone()


    @classmethod
    async def get_car_rides(cls, car_id: int):
        async with async_session() as session:
            try:
                query = (
                    select(
                        cls.model.car_id,
                        Ride,
                        RideInfo
                    )
                    .join(Ride, Ride.car_id == Car.car_id)
                    .join(RideInfo, Ride.ride_id == RideInfo.ride_id)
                    .where(cls.model.car_id == car_id)
                )
                result = await session.execute(query)

                return result.fetchall()
            except SQLAlchemyError as error:
                raise error


    @classmethod
    async def get_car_fixes(cls, car_id: int):
        async with async_session() as session:
            try:
                query = (
                    select(
                        cls.model.car_id,
                        FixInfo
                    )
                    .join(FixInfo, FixInfo.car_id == car_id)
                    .where(cls.model.car_id == car_id)
                )
                result = await session.execute(query)

                return result.fetchall()
            except SQLAlchemyError as error:
                raise error


    @classmethod
    async def get_car_predicted_data(cls, car_id: int):
        async with async_session() as session:
            try:
                query = (
                    select(
                        cls.model.car_id,
                        CarPredictedData.target_reg,
                        CarPredictedData.target_class
                    )
                    .where(CarPredictedData.car_id == car_id)
                )
                result = await session.execute(query)

                return result.fetchone()
            except SQLAlchemyError as error:
                raise error



