from app.infrastructure.db.database import async_session
from app.infrastructure.db.models.users import User
from app.repositories.repository import Repository

from sqlalchemy.future import select

class UserRepository(Repository):
    model = User


    @classmethod
    async def get_by_id(cls, user_id: int):
        async with async_session() as session:
            query = select(cls.model).where(cls.model.user_id == user_id)
            result = await session.execute(query)

            return result.scalar_one_or_none()


    @classmethod
    async def get_by_email(cls, email: str):
        async with async_session() as session:
            query = (
                select(
                    cls.model
                )
                .where(cls.model.email == email)
            )
            result = await session.execute(query)

            return result.scalar_one_or_none()