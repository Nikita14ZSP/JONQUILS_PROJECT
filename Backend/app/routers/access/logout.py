from fastapi import Response


async def logout(response: Response):
    response.delete_cookie(key="user_access_token")

    return {"message": "User successfully logged out"}