from datetime import datetime, date

from pydantic import (
    BaseModel,
    Field,
    field_validator
)


class SCarGet(BaseModel):
    car_id: int
    car_number: str
    is_rented: bool
    model: str
    car_type: str
    fuel_type: str
    car_rating: float
    year_to_start: int
    year_to_work: int
    rides: int


class SCarAdd(BaseModel):
    car_number: str = Field(..., description='Car number')
    is_rented: bool | None = Field(False, description='Is rented')
    model: str = Field(..., description='Car model')
    car_type: str = Field(..., description='Car type')
    fuel_type: str = Field(..., description='Fuel type')
    car_rating: float = Field(..., description='Car rating')
    year_to_start: int = Field(..., description='Year to start')
    year_to_work: int = Field(..., description='Year to work')
    rides: int = Field(..., description='Rides')


    @classmethod
    @field_validator('year_to_start')
    def validate_year_to_start(cls, year_to_start: int):
        current_year = datetime.now().year

        if year_to_start > current_year or year_to_start < 1900:
            raise ValueError('Year to start incorrect')

        return year_to_start


    @classmethod
    @field_validator('year_to_work')
    def validate_year_to_work(cls, year_to_work: int):
        current_year = datetime.now().year

        if year_to_work > current_year or year_to_work < 1900:
            raise ValueError('Year to work incorrect')

        return year_to_work


    @classmethod
    @field_validator('rides')
    def validate_rides(cls, rides: int):
        if rides < 0:
            raise ValueError('Rides must be positive')

        return rides


class SCarUpdate(BaseModel):
    car_number: str | None = Field(None, description='Car number')
    is_rented: bool | None = Field(None, description='Is rented')
    model: str | None = Field(None, description='Car model')
    car_type: str | None = Field(None, description='Car type')
    fuel_type: str | None = Field(None, description='Fuel type')
    car_rating: float | None = Field(None, description='Car rating')
    year_to_start: int | None = Field(None, description='Year to start')
    year_to_work: int | None = Field(None, description='Year to work')
    rides: int | None = Field(None, description='Rides')

    @classmethod
    @field_validator('year_to_start')
    def validate_year_to_start(cls, year_to_start: int):
        current_year = datetime.now().year

        if year_to_start and (year_to_start > current_year or year_to_start < 1900):
            raise ValueError('Year to start incorrect')

        return year_to_start

    @classmethod
    @field_validator('year_to_work')
    def validate_year_to_work(cls, year_to_work: int):
        current_year = datetime.now().year

        if year_to_work and (year_to_work > current_year or year_to_work < 1900):
            raise ValueError('Year to work incorrect')

        return year_to_work

    @classmethod
    @field_validator('rides')
    def validate_rides(cls, rides: int):
        if rides and rides < 0:
            raise ValueError('Rides must be positive')

        return rides


class SCarRidesGet(BaseModel):
    car_id: int
    driver_id: int
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


class SCarFixesGet(BaseModel):
    car_id: int
    mechanic_id: int
    fix_date: datetime
    work_type: str
    destroy_degree: float
    work_duration: int


class SCarWithPredictedDataGet(BaseModel):
    car_id: int
    car_number: str
    is_rented: bool
    model: str
    car_type: str
    fuel_type: str
    car_rating: float
    year_to_start: int
    year_to_work: int
    rides: int
    target_reg: float
    target_class: str


class SCarPredictedDataGet(BaseModel):
    car_id: int
    target_reg: float
    target_class: str

