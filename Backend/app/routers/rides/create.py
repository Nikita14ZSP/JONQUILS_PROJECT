from fastapi import (
    HTTPException,
    status,
    Response
)

from app.infrastructure.schemas.rides_schemas import SRideAdd
from app.repositories.ride_info_repository import RideInfoRepository
from app.repositories.ride_repository import RideRepository


async def add_ride(request: SRideAdd):
    try:
        ride_data = request.ride_data.model_dump()
        ride_info_data = request.ride_info_data.model_dump()

        ride = await RideRepository.add(**ride_data)

        ride_info_data['ride_id'] = ride.ride_id
        await RideInfoRepository.add(**ride_info_data)

        return {"message": "Ride added successfully", "ride_id": ride.ride_id}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))