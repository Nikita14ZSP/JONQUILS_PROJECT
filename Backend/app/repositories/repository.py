from sqlalchemy.future import select
from app.infrastructure.db.database import async_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update
from sqlalchemy import delete

class Repository:
    model = None


    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            query = select(cls.model).limit(100)
            result = await session.execute(query)

            return result.fetchall()


    @classmethod
    async def get_by_filter(cls, **filters):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)

            return result.scalars().all()


    @classmethod
    async def add(cls, **values):
        async with async_session() as session:
            async with session.begin():
                try:
                    new_instance = cls.model(**values)
                    session.add(new_instance)

                    await session.commit()

                    return new_instance
                except SQLAlchemyError as error:
                    await session.rollback()
                    raise error


    @classmethod
    async def update(cls, filters, **values):
        print(filters)
        print(values)
        async with async_session() as session:
            async with session.begin():
                try:
                    query = (
                        update(cls.model)
                        .where(*[getattr(cls.model, k) == v for k, v in filters.items()])
                        .values(**values)
                        .execution_options(synchronize_session="fetch")
                    )
                    await session.execute(query)

                    query = select(cls.model).where(*[getattr(cls.model, k) == v for k, v in filters.items()])
                    result = await session.execute(query)

                    await session.commit()

                    return result.fetchone()
                except SQLAlchemyError as error:
                    await session.rollback()
                    raise error


    @classmethod
    async def delete(cls, delete_all: bool = False, **filters):
        if not delete_all and not filters:
            raise ValueError("No filters provided")

        async with async_session() as session:
            async with session.begin():
                try:
                    query = delete(cls.model).filter_by(**filters)
                    result = await session.execute(query)

                    await session.commit()

                    return result.rowcount
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

