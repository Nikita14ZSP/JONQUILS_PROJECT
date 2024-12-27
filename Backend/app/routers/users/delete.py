from fastapi import HTTPException

from app.repositories.user_repository import UserRepository


async def delete(user_id: int):
    row_count = await UserRepository.delete(delete_all=False, user_id=user_id)

    if row_count > 0:
        return True

    raise HTTPException(status_code=404, detail="User not found")


