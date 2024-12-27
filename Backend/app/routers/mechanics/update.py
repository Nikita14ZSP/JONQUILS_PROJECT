from fastapi import (
    HTTPException,
    Path,
    Body,
    Depends
)

from app.authentication.get_current_user import get_current_user
from app.infrastructure.schemas.mechanic_schemas import SMechanicUpdate, SMechanicGet
from app.repositories.mechanic_repository import MechanicRepository
from app.repositories.user_repository import UserRepository


async def update(user_id: int, request_body: SMechanicUpdate):
    try:
        user_data = request_body.user_data.model_dump(exclude_none=True)
        mechanic_data = request_body.mechanic_data.model_dump(exclude_none=True)

        user = await UserRepository.update(
            {"user_id": user_id},
            **user_data
        )

        mechanic = await MechanicRepository.update(
            {"user_id": user_id},
            **mechanic_data
        )

        if user is None or mechanic is None:
            raise HTTPException(status_code=404, detail="Mechanic not found")

        return {"message": "Mechanic updated successfully", "mechanic_id": mechanic[0].mechanic_id}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


async def update_by_mechanic_id(mechanic_id: int = Path(...),  request_body: SMechanicUpdate = Body(...)):
    try:
        user = await MechanicRepository.get_by_filter(mechanic_id=mechanic_id)
        user = user[0]

        user_id = user.user_id
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

    return await update(user_id=user_id, request_body=request_body)


async def update_mechanic(request_body: SMechanicUpdate, current_user: SMechanicGet = Depends(get_current_user)):
    mechanic_data, _ = await MechanicRepository.get_by_mechanic_id(mechanic_id=current_user.mechanic_id)
    user_id = mechanic_data.user_id

    return await update(user_id=user_id, request_body=request_body)

