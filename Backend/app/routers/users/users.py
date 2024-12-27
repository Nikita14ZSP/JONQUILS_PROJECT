from fastapi import APIRouter

from app.routers.users.update import update_user

router = APIRouter(prefix='/users', tags=['Work with users (admins)'])

"""
It's route to Admin Update himself
Created to avoid code duplication
"""
router.add_api_route('/update', update_user, methods=['PUT'], summary='User update himself')