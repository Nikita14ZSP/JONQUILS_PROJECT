from fastapi import (
    HTTPException,
    status,
    Response
)

from app.authentication.passwords import get_password_hash
from app.authentication.tokens import create_access_token
from app.infrastructure.db.models.users import UserRoleEnum
from app.infrastructure.schemas.driver_schemas import SDriverRegistration
from app.infrastructure.schemas.mechanic_schemas import SMechanicRegistration
from app.infrastructure.schemas.user_schemas import SUserAdd
from app.repositories.driver_repository import DriverRepository
from app.repositories.mechanic_repository import MechanicRepository
from app.repositories.user_repository import UserRepository


async def admin_registration(data: SUserAdd):
    check = await UserRepository.get_by_filter(email=data.email)

    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

    user_data = data.model_dump()
    user_data['password_hash'] = get_password_hash(user_data['password_hash'])
    user_data['role'] = UserRoleEnum.ADMIN

    user = await UserRepository.add(**user_data)

    return {"message": "Admin registered successfully", "user_id": user.user_id}


async def driver_registration(response: Response, data: SDriverRegistration):
    response.delete_cookie(key="user_access_token")

    check = await UserRepository.get_by_filter(email=data.user_data.email)

    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

    user_data = data.user_data.model_dump()
    driver_data = data.driver_data.model_dump()

    user_data['password_hash'] = get_password_hash(user_data['password_hash'])
    user_data['role'] = UserRoleEnum.DRIVER
    user = await UserRepository.add(**user_data)

    driver_data['user_id'] = user.user_id
    driver = await DriverRepository.add(**driver_data)

    access_token = create_access_token({"sub": str(user.user_id)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True, secure=False)
    response.set_cookie(key="user_id", value=str(user.user_id), httponly=True, secure=False)
    response.set_cookie(key="role", value=str(user.role), httponly=True, secure=False)

    return {"message": "Driver registered successfully", "driver_id": driver.driver_id}


async def mechanic_registration(response: Response, data: SMechanicRegistration):
    response.delete_cookie(key="user_access_token")

    check = await UserRepository.get_by_filter(email=data.user_data.email)

    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

    user_data = data.user_data.model_dump()
    mechanic_data = data.mechanic_data.model_dump()

    user_data['password_hash'] = get_password_hash(user_data['password_hash'])
    user_data['role'] = UserRoleEnum.MECHANIC
    user = await UserRepository.add(**user_data)

    mechanic_data['user_id'] = user.user_id
    mechanic = await MechanicRepository.add(**mechanic_data)

    access_token = create_access_token({"sub": str(user.user_id)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True, secure=False)
    response.set_cookie(key="user_id", value=str(user.user_id), httponly=True, secure=False)
    response.set_cookie(key="role", value=str(user.role), httponly=True, secure=False)

    return {"message": "Mechanic registered successfully", "mechanic_id": mechanic.mechanic_id}