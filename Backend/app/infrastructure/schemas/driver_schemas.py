from app.infrastructure.db.models.users import UserSexEnum
from datetime import date

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)

from app.infrastructure.schemas.user_schemas import (
    SUserAdd,
    SUserUpdate
)


class SDriverGet(BaseModel):
    driver_id: int
    firstname: str
    lastname: str
    email: EmailStr
    age: int
    sex: UserSexEnum
    driver_rating: float
    driver_rides: int
    driver_time_accidents: int
    first_ride_date: date


class SDriverAdd(BaseModel):
    age: int = Field(..., description='Driver age')
    sex: UserSexEnum = Field(..., description='Driver sex')
    driver_rating: float = Field(...,description='Driver rating')
    driver_rides: int = Field(...,description='Driver rides')
    driver_time_accidents: int = Field(...,description='Driver time accidents')
    first_ride_date: date = Field(...,description='First ride date')

    @classmethod
    @field_validator('age')
    def validate_age(cls, age: int):
        if age < 0 or age > 105:
            raise ValueError('Age must be between 0 and 105.')

        return age


    @classmethod
    @field_validator('driver_rides')
    def validate_age(cls, driver_rides: int):
        if driver_rides < 0:
            raise ValueError('Driver rides must be positive.')

        return driver_rides

    @classmethod
    @field_validator('driver_time_accidents')
    def validate_age(cls, driver_time_accidents: int):
        if driver_time_accidents < 0:
            raise ValueError('Driver time accidents must be positive.')

        return driver_time_accidents


class SDriverRegistration(BaseModel):
    user_data: SUserAdd
    driver_data: SDriverAdd


class DriverUpdate(BaseModel):
    age: int | None = Field(None, description='Age')
    driver_rating: float | None = Field(None, description='Driver rating')
    driver_rides: int | None = Field(None, description='Driver rides')
    driver_time_accidents: int | None = Field(None, description='Driver time accidents')

    @classmethod
    @field_validator('age')
    def validate_age(cls, age: int):
        if age and (age < 0 or age > 105):
            raise ValueError('Age must be between 0 and 105.')

        return age

    @classmethod
    @field_validator('driver_rides')
    def validate_age(cls, driver_rides: int):
        if driver_rides and driver_rides < 0:
            raise ValueError('Driver rides must be positive.')

        return driver_rides

    @classmethod
    @field_validator('driver_time_accidents')
    def validate_age(cls, driver_time_accidents: int):
        if driver_time_accidents and driver_time_accidents < 0:
            raise ValueError('Driver time accidents must be positive.')

        return driver_time_accidents


class SDriverUpdate(BaseModel):
    user_data: SUserUpdate
    driver_data: DriverUpdate


class SDriverRidesGet(BaseModel):
    driver_id: int
    car_id: int
    rating: float
    ride_date: date
    ride_cost: int
    speed_avg: float
    speed_max: float
    stop_times: int
    distance: float
    refueling: int
    user_ride_quality: float
    deviation_normal: float

