from datetime import date, datetime

from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from app.infrastructure.schemas.ride_info_schemas import SRideInfoUpdate, SRideInfoAdd


class SRideGet(BaseModel):
    ride_id: int
    driver_id: int
    car_id: int
    rating: float
    ride_date: date
    ride_duration: int
    ride_cost: int
    speed_avg: float
    speed_max: float
    stop_times: int
    distance: float
    refueling: int
    user_ride_quality: float
    deviation_normal: float


class RideAdd(BaseModel):
    driver_id: int = Field(..., description='Driver ID')
    car_id: int = Field(..., description='Car ID')
    rating: float = Field(..., description='Rating')


    @classmethod
    @field_validator('rating')
    def validate_rating(cls, rating: float):
        if rating < 0 or rating > 10:
            raise ValueError('Rating must be between 0 and 10')

        return rating


class SRideAdd(BaseModel):
    ride_data: RideAdd
    ride_info_data: SRideInfoAdd


class RideUpdate(BaseModel):
    rating: float | None = Field(None, description='Rating')


    @classmethod
    @field_validator('rating')
    def validate_rating(cls, rating: float):
        if rating and (rating < 0 or rating > 10):
            raise ValueError('Rating must be between 0 and 10')

        return rating


class SRideUpdate(BaseModel):
    ride_data: RideUpdate
    ride_info_data: SRideInfoUpdate