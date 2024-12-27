import asyncio
import random
import string

from decimal import Decimal, InvalidOperation
from datetime import datetime
from random import randint

from faker import Faker

from app.authentication.passwords import get_password_hash
from app.infrastructure.db.models.cars_predicted_data import CarPredictedData
from app.repositories.car_predicted_data_repository import CarPredictedDataRepository
from app.repositories.car_repository import CarRepository
from app.repositories.driver_repository import DriverRepository
from app.repositories.fix_info_repository import FixInfoRepository
from app.repositories.mechanic_repository import MechanicRepository
from app.repositories.ride_info_repository import RideInfoRepository
from app.repositories.ride_repository import RideRepository
from app.repositories.user_repository import UserRepository

from app.infrastructure.db.models.users import (
    UserRoleEnum,
    UserSexEnum
)


CAR_INFO_FILE = './dataset/car_train.csv'
DRIVER_INFO_FILE = './dataset/driver_info.csv'
FIX_INFO_FILE = './dataset/fix_info.csv'
RIDES_INFO_FILE = './dataset/rides_info.csv'

fake = Faker()


def load_driver_ids():
    with open(DRIVER_INFO_FILE, 'r') as drivers_file:
        rows = drivers_file.readlines()[1:]

    driver_ids = set()
    for row in rows:
        fields = row.strip().split(',')
        driver_id = fields[4]
        driver_ids.add(driver_id)

    return {driver_id_str: driver_id_int for driver_id_int, driver_id_str in enumerate(driver_ids, start=1)}


def load_mechanic_ids():
    with open(FIX_INFO_FILE, 'r') as fix_info_file:
        rows = fix_info_file.readlines()[1:]

    mechanic_ids = set()
    for row in rows:
        fields = row.strip().split(',')
        mechanic_id = fields[1]
        mechanic_ids.add(mechanic_id)

    return {mechanic_id_str: mechanic_id_int for mechanic_id_int, mechanic_id_str in enumerate(mechanic_ids, start=1)}


def load_car_ids():
    with open(CAR_INFO_FILE, 'r') as car_file:
        rows = car_file.readlines()[1:]

    car_ids = set()
    for row in rows:
        fields = row.strip().split(',')
        car_id = fields[0]
        car_ids.add(car_id)

    return {car_id_str: car_id_int for car_id_int, car_id_str in enumerate(car_ids, start=1)}


def load_ride_ids():
    with open(RIDES_INFO_FILE, 'r') as rides_file:
        rows = rides_file.readlines()[1:]

    ride_ids = set()
    for row in rows:
        fields = row.strip().split(',')
        ride_id = fields[2]
        ride_ids.add(ride_id)

    return {ride_id_str: ride_id_int for ride_id_int, ride_id_str in enumerate(ride_ids, start=1)}


def generate_car_number():
    letters = string.ascii_uppercase  # Заглавные буквы
    region = random.randint(1, 99)  # Регион (от 1 до 99)
    number = (
        f"{random.choice(letters)}"
        f"{random.randint(100, 999)}"
        f"{random.choice(letters)}"
        f"{random.choice(letters)}"
      f"{region:02d}"
    )

    return number


async def fill_drivers_table():
    print("Start filling drivers table")

    with open(DRIVER_INFO_FILE, 'r') as drivers_file:
        rows = drivers_file.readlines()[1:]

    for row in rows:
        fields = row.strip().split(',')

        user_data = {
            'firstname': fake.first_name_male() if fields[5] == '1' else fake.first_name_female(),
            'lastname': fake.last_name(),
            'email': fake.email(),
            'password_hash': fake.password(),
            'role': UserRoleEnum.DRIVER
        }
        user_data['password_hash'] = get_password_hash(user_data['password_hash'])
        user = await UserRepository.add(**user_data)

        try:
            first_ride_date = datetime.strptime(fields[6], '%Y-%m-%d')
        except ValueError:
            first_ride_date = datetime.strptime(fake.date(), '%Y-%m-%d')

        driver_data = {
            'user_id': user.user_id,
            'driver_id': DRIVER_IDS[fields[4]],
            'age': int(fields[0]),
            'sex': UserSexEnum.MALE if fields[5] == '1' else UserSexEnum.FEMALE,
            'driver_rating': Decimal(fields[1]),
            'driver_rides': int(fields[2]),
            'driver_time_accidents': int(fields[3][:-2]) if fields[3] != '' else 0,
            'first_ride_date': first_ride_date
        }
        await DriverRepository.add(**driver_data)



async def fill_mechanics_table():
    print("Start filling mechanics table")

    for mechanic_id in MECHANIC_IDS.values():
        user_data = {
            'firstname': fake.first_name_male(),
            'lastname': fake.last_name(),
            'email': fake.email(),
            'password_hash': fake.password(),
            'role': UserRoleEnum.MECHANIC
        }
        user_data['password_hash'] = get_password_hash(user_data['password_hash'])
        user = await UserRepository.add(**user_data)

        mechanic_data = {
            'user_id': user.user_id,
            'mechanic_id': mechanic_id,
            'age': random.randint(18, 70),
            'sex': random.choice([UserSexEnum.MALE, UserSexEnum.FEMALE]),
            'mechanic_rating': random.randint(1, 10),
            'car_times_repaired': random.randint(1, 500)
        }
        await MechanicRepository.add(**mechanic_data)


async def fill_cars_table():
    print("Start filling cars table")

    with open(CAR_INFO_FILE, 'r') as car_info_file:
        rows = car_info_file.readlines()[1:]

    for row in rows:
        fields = row.strip().split(',')

        car_data = {
            'car_id': CAR_IDS[fields[0]],
            'car_number': generate_car_number(),
            'is_rented': False,
            'model': fields[1],
            'car_type': fields[2],
            'fuel_type': fields[3],
            'car_rating': Decimal(fields[4]),
            'year_to_start': int(fields[5]),
            'rides': int(fields[6]),
            'year_to_work': int(fields[7]),
        }
        car = await CarRepository.add(**car_data)

        car_predicted_data = {
            'car_id': car.car_id,
            'target_reg': Decimal(fields[8]),
            'target_class': fields[9]
        }
        await CarPredictedDataRepository.add(**car_predicted_data)


async def fill_rides_table():
    print("Start filling rides table")

    with open(RIDES_INFO_FILE, 'r') as ride_info_file:
        rows = ride_info_file.readlines()[1:]

    for row in rows:
        fields = row.strip().split(',')

        try:
            car_id = CAR_IDS[fields[1]]
            driver_id = DRIVER_IDS[fields[0]]
        except KeyError:
            continue

        try:
            rating = Decimal(fields[4])
        except (InvalidOperation, ValueError):
            rating = 7.0

        ride_data = {
            'driver_id': driver_id,
            'car_id': car_id,
            'rating': rating,
        }
        ride = await RideRepository.add(**ride_data)

        try:
            ride_date = datetime.strptime(fields[3], '%Y-%m-%d')
        except ValueError:
            ride_date = datetime.strptime(fake.date(), '%Y-%m-%d')

        try:
            speed_avg = Decimal(fields[7])
        except (InvalidOperation, ValueError):
            speed_avg = 70.0

        try:
            speed_max = Decimal(fields[8])
        except (InvalidOperation, ValueError):
            speed_max = 120.0

        try:
            distance = Decimal(fields[10])
        except (InvalidOperation, ValueError):
            distance = 350.5

        try:
            user_ride_quality = Decimal(fields[12])
        except (InvalidOperation, ValueError):
            user_ride_quality = random.uniform(-4, 4)

        try:
            deviation_normal = Decimal(fields[13])
        except (InvalidOperation, ValueError):
            deviation_normal = random.uniform(-4, 4)

        ride_info_data = {
            'ride_id': ride.ride_id,
            'ride_date': ride_date,
            'ride_duration': int(fields[5]),
            'ride_cost': int(fields[6]),
            'speed_avg': speed_avg,
            'speed_max': speed_max,
            'stop_times': int(fields[9]),
            'distance': distance,
            'refueling': int(fields[11]),
            'user_ride_quality': user_ride_quality,
            'deviation_normal': deviation_normal
        }
        await RideInfoRepository.add(**ride_info_data)


async def fill_fix_info_table():
    print("Start filling fixes table")

    with open(FIX_INFO_FILE, 'r') as fix_info_file:
        rows = fix_info_file.readlines()[1:]

    for row in rows:
        fields = row.strip().split(',')

        try:
            fix_date = datetime.strptime(fields[2], '%Y-%m-%d %H:%M')
        except ValueError:
            random_datetime = fake.date_time()  # Генерирует случайные дату и время
            fix_date = datetime.strptime(random_datetime.strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')

        try:
            car_id = CAR_IDS[fields[0]]
        except KeyError:
            continue

        fix_data = {
            'car_id': car_id,
            'mechanic_id': MECHANIC_IDS[fields[1]],
            'fix_date': fix_date,
            'work_type': fields[3],
            'destroy_degree': Decimal(fields[4]),
            'work_duration': int(fields[5])
        }
        await FixInfoRepository.add(**fix_data)


if __name__ == '__main__':
    print("Start filling tables")

    global DRIVER_IDS
    global MECHANIC_IDS
    global CAR_IDS
    global RIDE_IDS

    DRIVER_IDS = load_driver_ids()
    MECHANIC_IDS = load_mechanic_ids()
    CAR_IDS = load_car_ids()
    RIDE_IDS = load_ride_ids()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(fill_rides_table())
    finally:
        loop.close()

    #asyncio.run(fill_drivers_table())
    #asyncio.run(fill_mechanics_table())
    #asyncio.run(fill_cars_table())
    #asyncio.run(fill_rides_table())
    #asyncio.run(fill_fix_info_table())

    print("All tables filled successfully")