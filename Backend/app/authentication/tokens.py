from jose import jwt

from datetime import (
    datetime,
    timedelta,
    timezone
)

from fastapi import (
    Request,
    HTTPException,
    status
)

from app.config.config import get_jwt_settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=2)
    to_encode.update({"exp": expire})

    jwt_params = get_jwt_settings()
    encoded_jwt = jwt.encode(to_encode, jwt_params['secret_key'], algorithm=jwt_params['algorithm'])

    return encoded_jwt


def get_token(request: Request) -> str:
    token = request.cookies.get('token')

    if not token:
        token = request.headers.get('Authorization')

        if token and token.startswith('Bearer '):
            token = token.split(" ")[1]

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is missing')

    return token