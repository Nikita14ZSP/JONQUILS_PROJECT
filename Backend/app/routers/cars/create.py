from fastapi import Depends, HTTPException

from app.infrastructure.schemas.car_schemas import SCarAdd
from app.repositories.car_repository import CarRepository


async def add_car(request: SCarAdd):
    try:
        car_data = request.model_dump()
        car = await CarRepository.add(**car_data)

        return {"message": "Car added successfully", "car_id": car.car_id}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

