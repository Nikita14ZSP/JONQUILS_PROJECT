from fastapi import APIRouter

from app.routers.rides.create import add_ride
from app.routers.rides.delete import delete_by_id
from app.routers.rides.read import get_all_rides, get_ride_by_id
from app.routers.rides.update import update_ride

router = APIRouter(prefix='/rides', tags=['Work with rides'])

router.add_api_route('/add', add_ride, methods=['POST'], summary='Add ride')

router.add_api_route('/get_all', get_all_rides, methods=['GET'], summary='Get all rides')
router.add_api_route('/get_by_id/{ride_id}', get_ride_by_id, methods=['GET'], summary='Get one ride by id')

router.add_api_route('/delete/{ride_id}', delete_by_id, methods=['DELETE'], summary='Delete one ride')

router.add_api_route('/update/{ride_id}', update_ride, methods=['PUT'], summary='Update one ride')



