from fastapi import APIRouter

from app.routers.cars.create import add_car
from app.routers.cars.delete import delete_by_car_id, delete_car_predicted_data_by_car_id
from app.routers.cars.read import get_all_cars, get_all_cars_with_predict, get_car_by_id, get_car_by_id_with_predict, \
    get_car_predicted_data, get_car_rides, get_car_fixes
from app.routers.cars.update import update_car_by_id, update_car_predicted_data_by_id, run_ml_model

router = APIRouter(prefix="/cars", tags=["Work with cars"])

router.add_api_route('/add', add_car, methods=['POST'], summary='Add one car')

router.add_api_route('/get_all', get_all_cars, methods=['GET'], summary='Get all cars')
router.add_api_route(
    '/get_all_with_predict',
    get_all_cars_with_predict,
    methods=['GET'],
    summary='Get all cars with predicted data'
)

router.add_api_route('/get_by_id/{car_id}', get_car_by_id, methods=['GET'], summary='Get one car by id')
router.add_api_route(
    '/get_by_id_with_predict/{car_id}',
    get_car_by_id_with_predict,
    methods=['GET'],
    summary='Get one car by id with predicted data'
)

router.add_api_route(
    '/get_predict_data/{car_id}',
    get_car_predicted_data,
    methods=['GET'],
    summary='Get one car predicted data'
)


router.add_api_route('/get_rides', get_car_rides, methods=['GET'], summary='Get car all rides')
router.add_api_route('/get_fixes', get_car_fixes, methods=['GET'], summary='Get car all fixes')
router.add_api_route('/predict_cars_data', run_ml_model, methods=['GET'], summary='Run ML service')

router.add_api_route('/delete/{car_id}', delete_by_car_id, methods=['DELETE'], summary='Delete one car by id')
router.add_api_route(
    '/delete/predicted_data/{car_id}',
    delete_car_predicted_data_by_car_id,
    methods=['DELETE'],
    summary='Delete one car predicted data'
)

router.add_api_route('/update/{car_id}', update_car_by_id, methods=['PUT'], summary='Update one car by id')
router.add_api_route(
    '/update/predicted_data/{car_id}',
    update_car_predicted_data_by_id,
    methods=['PUT'],
    summary='Update one car predicted data'
)