from datetime import date, datetime

from pydantic import (
    BaseModel,
    Field,
    field_validator
)


class SRideInfoGet(BaseModel):
    ride_id: int
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


class SRideInfoAdd(BaseModel):
    ride_date: date = Field(..., description='Date of ride')
    ride_duration: int = Field(..., description='Duration of ride')
    ride_cost: int = Field(..., description='Cost of ride')
    speed_avg: float = Field(..., description='Average speed of ride')
    speed_max: float = Field(..., description='Max speed of ride')
    stop_times: int = Field(..., description='Number of stops')
    distance: float = Field(..., description='Distance')
    refueling: int = Field(..., description='Number of refueling')
    user_ride_quality: float = Field(..., description='Quality of user ride')
    deviation_normal: float = Field(..., description='Normal deviation')


    @classmethod
    @field_validator('ride_date')
    def validate_ride_date(cls, ride_date: date):
        current_date = datetime.now().date()

        if ride_date > current_date:
            raise ValueError('Ride date cannot be in the future')

        return ride_date


    @classmethod
    @field_validator('ride_duration')
    def validate_rides(cls, ride_duration: int):
        if ride_duration < 0:
            raise ValueError('Ride duration must be positive')

        return ride_duration


    @classmethod
    @field_validator('ride_cost')
    def validate_rides(cls, ride_cost: int):
        if ride_cost < 0:
            raise ValueError('Ride cost must be positive')

        return ride_cost


class SRideInfoUpdate(BaseModel):
    ride_date: date | None = Field(None, description='Date of ride')
    ride_duration: int | None = Field(None, description='Duration of ride')
    ride_cost: int | None = Field(None, description='Cost of ride')
    speed_avg: float | None = Field(None, description='Average speed of ride')
    speed_max: float | None = Field(None, description='Max speed of ride')
    stop_times: int | None = Field(None, description='Number of stops')
    distance: float | None = Field(None, description='Distance')
    refueling: int | None = Field(None, description='Number of refueling')
    user_ride_quality: float | None = Field(None, description='Quality of user ride')
    deviation_normal: float | None = Field(None, description='Normal deviation')


    @classmethod
    @field_validator('ride_date')
    def validate_ride_date(cls, ride_date: date):
        current_date = datetime.now().date()

        if ride_date and ride_date > current_date:
            raise ValueError('Ride date cannot be in the future')

        return ride_date


    @classmethod
    @field_validator('ride_duration')
    def validate_rides(cls, ride_duration: int):
        if ride_duration and ride_duration < 0:
            raise ValueError('Ride duration must be positive')

        return ride_duration


    @classmethod
    @field_validator('ride_cost')
    def validate_rides(cls, ride_cost: int):
        if ride_cost and ride_cost < 0:
            raise ValueError('Ride cost must be positive')

        return ride_cost

