from fastapi import APIRouter

from app.routers.access.profile import get_profile
from app.routers.access.login import login
from app.routers.access.logout import logout
from app.routers.access.registration import (
    admin_registration,
    driver_registration,
    mechanic_registration
)


router = APIRouter(prefix='/access', tags=['Work with Access to Application'])

router.add_api_route(
    "/registration/admin",
    admin_registration,
    methods=["POST"],
    summary="Admin Registration (Adding)"
)

router.add_api_route(
    "/registration/driver",
    driver_registration,
    methods=["POST"],
    summary="Driver Registration"
)

router.add_api_route(
    "/registration/mechanic",
    mechanic_registration,
    methods=["POST"],
    summary="Mechanic Registration"
)

router.add_api_route("/login", login, methods=["POST"], summary="Login")
router.add_api_route("/logout", logout, methods=["POST"], summary="Logout")
router.add_api_route("/profile", get_profile, methods=["GET"], summary="Profile")

