from fastapi import APIRouter

from app.routers.fixes.create import add_fix_info
from app.routers.fixes.delete import delete_by_id
from app.routers.fixes.read import get_all_fixes, get_by_fix_id
from app.routers.fixes.update import update_fix_by_id

router = APIRouter(prefix='/fixes', tags=['Work with fixes'])

router.add_api_route('/add', add_fix_info, methods=['POST'], summary='Add fix info')

router.add_api_route('/get_all', get_all_fixes, methods=["GET"], summary="Get all fixes")
router.add_api_route('/get_by_id/{fix_info_id}', get_by_fix_id, methods=["GET"], summary="Get one fix by id")

router.add_api_route('/delete/{fix_info_id}', delete_by_id, methods=["DELETE"], summary="Delete one fix by id")

router.add_api_route('/update/{fix_info_id}', update_fix_by_id, methods=["PUT"], summary="Update one fix by id")
