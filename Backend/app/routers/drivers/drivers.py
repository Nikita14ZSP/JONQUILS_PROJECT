from fastapi import APIRouter

from app.routers.drivers.delete import delete_driver, delete_by_driver_id
from app.routers.drivers.read import get_all_drivers, get_driver_by_id, get_driver_rides
from app.routers.drivers.update import update_driver, update_by_driver_id

router = APIRouter(prefix='/drivers', tags=['Work with drivers'])

router.add_api_route("/get_all", get_all_drivers, methods=["GET"], summary="Get all drivers")
router.add_api_route("/get_by_id/{driver_id}", get_driver_by_id, methods=["GET"], summary="Get one driver by id")
router.add_api_route("/get_rides/{driver_id}", get_driver_rides, methods=["GET"], summary="Get driver rides")

router.add_api_route("/delete", delete_driver, methods=["DELETE"], summary="Delete one driver himself")
router.add_api_route(
    "/delete_by_id/{driver_id}",
    delete_by_driver_id,
    methods=["DELETE"],
    summary="Delete one driver by id"
)

router.add_api_route("/update", update_driver, methods=["PUT"], summary="Driver update information about himself")
router.add_api_route("/update_by_id/{driver_id}", update_by_driver_id, methods=["PUT"], summary="Update one driver by id")

