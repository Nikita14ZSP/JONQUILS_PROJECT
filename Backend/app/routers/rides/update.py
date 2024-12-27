from fastapi import (
    HTTPException,
    Path,
    Body,
    Depends
)


from app.infrastructure.schemas.rides_schemas import SRideUpdate
from app.repositories.ride_repository import RideRepository
from app.repositories.ride_info_repository import RideInfoRepository


async def update_ride(ride_id: int = Path(...), request_body: SRideUpdate = Body(...)):
    try:
        ride_data = request_body.ride_data.model_dump()
        ride_info_data = request_body.ride_info_data.model_dump()

        ride_info_data = {key: value for key, value in ride_info_data.items() if value is not None}

        ride = await RideRepository.update(
            {"ride_id": ride_id},
            **ride_data
        )

        ride_info = await RideInfoRepository.update(
            {"ride_id": ride_id},
            **ride_info_data
        )

        if ride is None or ride_info is None:
            raise HTTPException(status_code=404, detail="Ride not found")

        return {"message": "Ride updated successfully", "ride_id": ride[0].ride_id}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))