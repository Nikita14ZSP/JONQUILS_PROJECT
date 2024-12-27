from fastapi import HTTPException, status, Response

from app.authentication.authenticate_user import authenticate_user
from app.authentication.tokens import create_access_token
from app.infrastructure.schemas.user_schemas import SUserAuth


async def login(response: Response, user_data: SUserAuth):
    user_info = await authenticate_user(email=user_data.email, password=user_data.password)

    if user_info is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')

    access_token = create_access_token({"sub": str(user_info["user_id"])})

    response.delete_cookie(key='user_access_token')
    response.set_cookie(key="user_access_token", value=access_token, httponly=True, secure=False)
    response.set_cookie(key="user_id", value=str(user_info["user_id"]), httponly=True, secure=False)
    response.set_cookie(key="role", value=str(user_info["role"]), httponly=True, secure=False)

    return {
        "access_token": access_token,
        "refresh_token": None,
        "role": str(user_info["role"])
    }

