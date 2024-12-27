from fastapi import (
    Path,
    HTTPException,
    Depends
)

from app.repositories.fix_info_repository import FixInfoRepository


async def delete_by_id(fix_info_id: int = Path(...)):
    row_count = await FixInfoRepository.delete(delete_all=False, fix_info_id=fix_info_id)

    if row_count > 0:
        return True

    raise HTTPException(status_code=404, detail="Fix not found")