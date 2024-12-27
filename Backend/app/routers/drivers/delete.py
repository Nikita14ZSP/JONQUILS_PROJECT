from fastapi import (
    Path,
    HTTPException,
    Depends
)

from app.authentication.get_current_user import get_current_user
from app.infrastructure.schemas.driver_schemas import SDriverGet
from app.repositories.driver_repository import DriverRepository
from app.routers.users.delete import delete


async def delete_by_driver_id(driver_id: int = Path(...)):
    try:
        user = await DriverRepository.get_by_filter(driver_id=driver_id)
        user = user[0]

        user_id = user.user_id
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

    return await delete(user_id=user_id)


async def delete_driver(current_user: SDriverGet = Depends(get_current_user)):
    return await delete(user_id=current_user.user_id)