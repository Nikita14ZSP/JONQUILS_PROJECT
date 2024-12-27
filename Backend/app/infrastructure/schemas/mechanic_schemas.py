from datetime import datetime

from app.infrastructure.db.models.users import UserSexEnum

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


class SMechanicGet(BaseModel):
    mechanic_id: int
    firstname: str
    lastname: str
    email: EmailStr
    age: int
    sex: UserSexEnum
    mechanic_rating: float
    car_times_repaired: int


class SMechanicAdd(BaseModel):
    age: int = Field(..., description='Mechanic age')
    sex: UserSexEnum = Field(..., description='Mechanic sex')
    mechanic_rating: float = Field(..., description='Mechanic rating')
    car_times_repaired: int = Field(..., description='Mechanic car times repaired')


    @classmethod
    @field_validator('age')
    def validate_age(cls, age: int):
        if age < 0 or age > 105:
            raise ValueError('Age must be between 0 and 105.')

        return age


    @classmethod
    @field_validator('car_times_repaired')
    def validate_car_times_repaired(cls, car_times_repaired: int):
        if car_times_repaired < 0:
            raise ValueError('Car times repaired must be positive.')


class SMechanicRegistration(BaseModel):
    user_data: SUserAdd
    mechanic_data: SMechanicAdd


class MechanicUpdate(BaseModel):
    age: int | None = Field(None, description='Age')
    mechanic_rating: float | None = Field(None, description='Mechanic rating')
    car_times_repaired: int | None = Field(None, description='Mechanic car times repaired')


    @classmethod
    @field_validator('age')
    def validate_age(cls, age: int):
        if age and (age < 0 or age > 105):
            raise ValueError('Age must be between 0 and 105.')

        return age


    @classmethod
    @field_validator('car_times_repaired')
    def validate_car_times_repaired(cls, car_times_repaired: int):
        if car_times_repaired and car_times_repaired < 0:
            raise ValueError('Car times repaired must be positive.')


class SMechanicUpdate(BaseModel):
    user_data: SUserUpdate
    mechanic_data: MechanicUpdate


class SMechanicFixesGet(BaseModel):
    mechanic_id: int
    car_id: int
    fix_date: datetime
    work_type: str
    destroy_degree: float
    work_duration: int
    car_number: str
    model: str
    car_type: str
    fuel_type: str
    year_to_start: int
    year_to_work: int
    rides: int

