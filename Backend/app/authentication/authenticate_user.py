from pydantic import EmailStr

from app.repositories.user_repository import UserRepository
from app.authentication.passwords import verify_password


async def authenticate_user(email: EmailStr, password: str):
    user = await UserRepository.get_by_email(email=email)

    if user is None:
        print('User not found')
        return None

    if verify_password(plain_password=password, hashed_password=user.password_hash) is False:
        print('Invalid password')
        return None

    return {
        "user_id": user.user_id,
        "role": user.role
    }