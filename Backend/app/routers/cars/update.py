import httpx

from fastapi import (
    HTTPException,
    Path,
    Body,
    Depends
)
import requests
from app.config.config import get_ml_server_query_url
from app.infrastructure.schemas.car_schemas import SCarUpdate
from app.infrastructure.schemas.cars_predicted_data_schemas import SCarPredictedDataUpdate
from app.repositories.car_repository import CarRepository
from app.repositories.car_predicted_data_repository import CarPredictedDataRepository


async def update_car_by_id(car_id: int = Path(...), request_body: SCarUpdate = Body(...)):
    try:
        car_data = request_body.model_dump(exclude_none=True)

        car = await CarRepository.update(
            {"car_id": car_id},
            **car_data
        )

        if car is None:
            raise HTTPException(status_code=404, detail="Car not found")

        return {"message": "Car updated successfully", "car_id": car[0].car_id}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


async def update_car_predicted_data_by_id(car_id: int = Path(...), request_body: SCarPredictedDataUpdate = Body(...)):
    try:
        update_data = request_body.model_dump(exclude_none=True)

        car_predicted_data = await CarPredictedDataRepository.update(
            {"car_id": car_id},
            **update_data
        )

        if car_predicted_data is None:
            raise HTTPException(status_code=404, detail="Car Predicted Data not found")

        return {"message": "Car Predicted Data updated successfully", "car_id": car_predicted_data.car_id}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


async def run_ml_model():
    ml_server_query_url = get_ml_server_query_url()

    try:
        response = requests.get(ml_server_query_url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except httpx.ConnectError as error:
        print(f"Connection error: {error}")
    except httpx.RequestError as error:
        print(f"Request error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")

    return {"message": "Ml server started successfully"}