from fastapi import (
    HTTPException,
    Depends
)

from app.authentication.get_current_user import get_current_user
from app.infrastructure.schemas.user_schemas import SUserUpdate, SUserGet
from app.repositories.user_repository import UserRepository


async def update_user(request_body: SUserUpdate, current_user: SUserGet = Depends(get_current_user)):
    try:
        user_id = current_user.user_id
        user_data = request_body.model_dump(exclude_none=True)

        user = await UserRepository.update(
            {"user_id": user_id},
            **user_data
        )

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User updated successfully", "user_id": user[0].user_id}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
