from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncAttrs
)

from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr
)

from app.config.config import get_db_url


DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=True)


class BaseTable(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        name = cls.__name__
        table_name = ""

        if name == "User":
            table_name = "users"
        elif name == "Driver":
            table_name = "drivers"
        elif name == "Mechanic":
            table_name = "mechanics"
        elif name == "Car":
            table_name = "cars"
        elif name == "CarPredictedData":
            table_name = "cars_predicted_data"
        elif name == "Ride":
            table_name = "rides"
        elif name == "RideInfo":
            table_name = "ride_info"
        elif name == "FixInfo":
            table_name = "fix_info"

        return table_name

