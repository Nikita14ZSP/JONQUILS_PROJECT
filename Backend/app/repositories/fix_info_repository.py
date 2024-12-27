from app.infrastructure.db.database import async_session
from app.infrastructure.db.models.fix_info import FixInfo
from app.repositories.repository import Repository

from sqlalchemy.future import select


class FixInfoRepository(Repository):
    model = FixInfo

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
    async def get_by_id(cls, fix_info_id: int):
        async with async_session() as session:
            query = (
                select(
                    cls.model
                )
                .where(cls.model.fix_info_id == fix_info_id)
            )
            result = await session.execute(query)

            return result.fetchone()

