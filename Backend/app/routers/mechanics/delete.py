from fastapi import (
    Path,
    HTTPException,
    Depends
)

from app.authentication.get_current_user import get_current_user
from app.infrastructure.schemas.mechanic_schemas import SMechanicGet
from app.repositories.mechanic_repository import MechanicRepository
from app.routers.users.delete import delete


async def delete_by_mechanic_id(mechanic_id: int = Path(...)):
    try:
        user = await MechanicRepository.get_by_filter(mechanic_id=mechanic_id)

        if not user:
            raise HTTPException(status_code=404, detail="Mechanic not found")

        user = user[0]

        user_id = user.user_id
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

    return await delete(user_id=user_id)


async def delete_mechanic(current_user: SMechanicGet = Depends(get_current_user)):
    return await delete(user_id=current_user.user_id)