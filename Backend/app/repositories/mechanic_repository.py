from app.infrastructure.db.database import async_session
from app.infrastructure.db.models.mechanics import Mechanic
from app.infrastructure.db.models.cars import Car
from app.infrastructure.db.models.fix_info import FixInfo
from app.infrastructure.db.models.users import User
from app.repositories.repository import Repository

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError


class MechanicRepository(Repository):
    model = Mechanic


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
    async def get_by_mechanic_id(cls, mechanic_id: int):
        async with async_session() as session:
            query = (
                select(
                    cls.model,
                    User
                )
                .join(User, User.user_id == cls.model.user_id)
                .where(cls.model.mechanic_id == mechanic_id)
            )
            result = await session.execute(query)

            return result.fetchone()


    @classmethod
    async def get_mechanic_fixes(cls, mechanic_id: int):
        async with async_session() as session:
            try:
                query = (
                    select(
                        cls.model.mechanic_id,
                        FixInfo,
                        Car
                    )
                    .join(FixInfo, FixInfo.mechanic_id == Mechanic.mechanic_id)
                    .join(Car, FixInfo.car_id == Car.car_id)
                    .where(cls.model.mechanic_id == mechanic_id)
                )
                fixes = await session.execute(query)

                return fixes.fetchall()
            except SQLAlchemyError as error:
                raise error

