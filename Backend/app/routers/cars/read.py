from app.infrastructure.schemas.car_schemas import SCarGet, SCarPredictedDataGet, SCarWithPredictedDataGet, \
    SCarFixesGet, SCarRidesGet
from app.repositories.car_repository import CarRepository


async def get_all_cars():
    cars = await CarRepository.get_all()

    cars = [
        SCarGet(
            **car_data[0].__dict__
        ) for car_data in cars
    ]

    return cars


async def get_all_cars_with_predict():
    cars = await CarRepository.get_all_with_predict()

    cars = [
        SCarWithPredictedDataGet(
            **{
                **car_data.__dict__,
                **car_predicted_data.__dict__
            }
        ) for (car_data, car_predicted_data) in cars
    ]

    return cars


async def get_car_by_id(car_id: int):
    car = await CarRepository.get_by_id(car_id=car_id)
    car_data = car[0]

    return SCarGet(**car_data.__dict__)


async def get_car_by_id_with_predict(car_id: int):
    car = await CarRepository.get_by_id_with_predict(car_id=car_id)

    car_data, car_predicted_data = car
    car_dict = {**car_data.__dict__, **car_predicted_data.__dict__}

    return SCarWithPredictedDataGet(**car_dict)


async def get_car_predicted_data(car_id: int):
    car_predicted_data = await CarRepository.get_car_predicted_data(car_id=car_id)
    car_pred_data = car_predicted_data[0]

    return SCarPredictedDataGet(**car_pred_data.__dict__)


async def get_car_rides(car_id: int):
    car_rides = await CarRepository.get_car_rides(car_id=car_id)

    car_rides = [
        SCarRidesGet(
            **{
                **ride_data.__dict__,
                **ride_info_data.__dict__
            }
        ) for _, ride_data, ride_info_data in car_rides
    ]

    return car_rides


async def get_car_fixes(car_id: int):
    car_fixes = await CarRepository.get_car_fixes(car_id=car_id)

    car_fixes = [
        SCarFixesGet(
            **fix_data.__dict__
        ) for _, fix_data in car_fixes
    ]

    return car_fixes
