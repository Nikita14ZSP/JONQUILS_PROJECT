from fastapi import (
    Path,
    HTTPException,
    Depends
)

from app.repositories.ride_repository import RideRepository


async def delete_by_id(ride_id: int = Path(...)):
    row_count = await RideRepository.delete(delete_all=False, ride_id=ride_id)

    if row_count > 0:
        return True

    raise HTTPException(status_code=404, detail="Fix not found")