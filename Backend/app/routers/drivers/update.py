from fastapi import (
    HTTPException,
    Path,
    Body,
    Depends
)

from app.authentication.get_current_user import get_current_user
from app.infrastructure.schemas.driver_schemas import SDriverUpdate, SDriverGet
from app.repositories.driver_repository import DriverRepository
from app.repositories.user_repository import UserRepository


async def update(user_id: int, request_body: SDriverUpdate):
    try:
        user_data = request_body.user_data.model_dump(exclude_none=True)
        driver_data = request_body.driver_data.model_dump(exclude_none=True)

        user = await UserRepository.update(
            {"user_id": user_id},
            **user_data
        )

        driver = await DriverRepository.update(
            {"user_id": user_id},
            **driver_data
        )

        if user is None or driver is None:
            raise HTTPException(status_code=404, detail="Driver not found")

        return {"message": "Driver updated successfully", "driver_id": driver[0].driver_id}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


async def update_by_driver_id(driver_id: int = Path(...),  request_body: SDriverUpdate = Body(...)):
    try:
        user = await DriverRepository.get_by_filter(driver_id=driver_id)
        user = user[0]

        user_id = user.user_id
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

    return await update(user_id=user_id, request_body=request_body)


async def update_driver(request_body: SDriverUpdate, current_user: SDriverGet = Depends(get_current_user)):
    drivar_data, _ = await DriverRepository.get_by_driver_id(current_user.driver_id)
    user_id = drivar_data.user_id

    return await update(user_id=user_id, request_body=request_body)