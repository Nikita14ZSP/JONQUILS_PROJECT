from app.infrastructure.schemas.rides_schemas import SRideGet
from app.repositories.ride_repository import RideRepository


async def get_all_rides():
    rides = await RideRepository.get_all()

    rides = [
        SRideGet(
            **{
                **ride_data.__dict__,
                **ride_info_data.__dict__
            }
        ) for (ride_data, ride_info_data) in rides
    ]

    return rides


async def get_ride_by_id(ride_id: int):
    ride = await RideRepository.get_by_id(ride_id=ride_id)

    ride_data, ride_info_data = ride
    ride_dict = {**ride_data.__dict__, **ride_info_data.__dict__}

    return SRideGet(**ride_dict)

