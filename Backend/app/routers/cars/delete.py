from fastapi import (
    Path,
    HTTPException,
    Depends
)

from app.repositories.car_predicted_data_repository import CarPredictedDataRepository
from app.repositories.car_repository import CarRepository


async def delete_by_car_id(car_id: int = Path(...)):
    row_count = await CarRepository.delete(delete_all=False, car_id=car_id)

    if row_count > 0:
        return True

    raise HTTPException(status_code=404, detail="Car not found")


async def delete_car_predicted_data_by_car_id(car_id: int = Path(...)):
    row_count = await CarPredictedDataRepository.delete(delete_all=False, car_id=car_id)

    if row_count > 0:
        return True

    raise HTTPException(status_code=404, detail="Car not found")