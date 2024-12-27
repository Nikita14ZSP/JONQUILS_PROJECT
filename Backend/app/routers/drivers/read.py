from app.infrastructure.schemas.driver_schemas import SDriverGet, SDriverRidesGet
from app.repositories.driver_repository import DriverRepository


async def get_all_drivers():
    drivers = await DriverRepository.get_all()

    drivers = [
        SDriverGet(
            **{
                **driver_data.__dict__,
                **user_data.__dict__
            }
        ) for (driver_data, user_data) in drivers
    ]

    return drivers


async def get_driver_by_id(driver_id: int):
    driver = await DriverRepository.get_by_driver_id(driver_id=driver_id)

    driver_data, user_data = driver
    driver_dict = {**driver_data.__dict__, **user_data.__dict__}

    return SDriverGet(**driver_dict)


async def get_driver_rides(driver_id: int):
    driver_rides = await DriverRepository.get_driver_rides(driver_id=driver_id)

    driver_rides = [
        SDriverRidesGet(
            **{
                **ride_data.__dict__,
                **ride_info_data.__dict__
            }
        ) for (driver_id, ride_data, ride_info_data) in driver_rides
    ]

    return driver_rides

