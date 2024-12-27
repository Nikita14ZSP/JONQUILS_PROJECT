from fastapi import (
    HTTPException,
    status,
    Depends
)

from jose import (
    jwt,
    JWTError
)

from datetime import (
    datetime,
    timezone
)

from app.authentication.tokens import get_token
from app.config.config import get_jwt_settings
from app.infrastructure.db.models.users import UserRoleEnum
from app.infrastructure.schemas.driver_schemas import SDriverGet
from app.infrastructure.schemas.mechanic_schemas import SMechanicGet
from app.infrastructure.schemas.user_schemas import SUserGet
from app.repositories.driver_repository import DriverRepository
from app.repositories.mechanic_repository import MechanicRepository
from app.repositories.user_repository import UserRepository


async def get_current_user(token: str = Depends(get_token)):
    print("INFO: get_current_user_started")

    try:
        jwt_settings = get_jwt_settings()
        payload = jwt.decode(token, jwt_settings['secret_key'], algorithms=[jwt_settings['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)

    if not expire or expire_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired')

    user_id = payload.get('sub')

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User ID is missing')

    user = await UserRepository.get_by_id(user_id=int(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    if user.role == UserRoleEnum.ADMIN:
        user_data = user[0]
        user_dict = {**user_data.__dict__}

        return SUserGet(**user_dict)
    elif user.role == UserRoleEnum.DRIVER:
        driver = await DriverRepository.get_by_user_id(user_id=int(user_id))

        driver_data, user_data = driver
        driver_dict = {**driver_data.__dict__, **user_data.__dict__}

        return SDriverGet(**driver_dict)
    elif user.role == UserRoleEnum.MECHANIC:
        mechanic = await MechanicRepository.get_by_user_id(user_id=int(user_id))

        mechanic_data, user_data = mechanic
        mechanic_dict = {**mechanic_data.__dict__, **user_data.__dict__}

        return SMechanicGet(**mechanic_dict)
