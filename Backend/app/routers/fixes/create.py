from fastapi import Depends, HTTPException

from app.infrastructure.schemas.fix_info_schemas import SFixInfoAdd
from app.repositories.fix_info_repository import FixInfoRepository


async def add_fix_info(request: SFixInfoAdd):
    try:
        fix_data = request.model_dump()
        fix_data['fix_date'] = fix_data['fix_date'].replace(tzinfo=None)

        fix = await FixInfoRepository.add(**fix_data)

        return {"message": "Fix added successfully", "fix_info_id": fix.fix_info_id}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))