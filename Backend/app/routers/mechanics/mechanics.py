from fastapi import APIRouter

from app.routers.mechanics.delete import delete_mechanic, delete_by_mechanic_id
from app.routers.mechanics.read import get_all_mechanics, get_mechanic_by_id, get_mechanic_fixes
from app.routers.mechanics.update import update_mechanic, update_by_mechanic_id

router = APIRouter(prefix='/mechanics', tags=['Work with mechanics'])

router.add_api_route('/get_all', get_all_mechanics, methods=['GET'], summary='Get all mechanics')
router.add_api_route('/get_by_id/{mechanic_id}', get_mechanic_by_id, methods=['GET'], summary='Get one mechanic by id')
router.add_api_route('/get_fixes/{mechanic_id}', get_mechanic_fixes, methods=['GET'], summary='Get all mechanic fixes')

router.add_api_route('/delete', delete_mechanic, methods=['DELETE'], summary='Delete one mechanic himself')
router.add_api_route(
    '/delete_by_id/{mechanic_id}',
    delete_by_mechanic_id,
    methods=['DELETE'],
    summary="Delete one mechanic by id"
)

router.add_api_route('/update', update_mechanic, methods=['PUT'], summary='Mechanic update information about himself')
router.add_api_route('/update_by_id/{mechanic_id}', update_by_mechanic_id, methods=['PUT'], summary='Update one mechanic by id')

