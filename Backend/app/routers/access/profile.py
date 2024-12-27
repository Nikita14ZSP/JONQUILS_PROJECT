from typing import Union

from fastapi import Depends

from app.authentication.get_current_user import get_current_user
from app.infrastructure.schemas.driver_schemas import SDriverGet
from app.infrastructure.schemas.mechanic_schemas import SMechanicGet
from app.infrastructure.schemas.user_schemas import SUserGet


async def get_profile(user_data: Union[SUserGet, SDriverGet, SMechanicGet] = Depends(get_current_user)):
    return user_data

