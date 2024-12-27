from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)


class SFixInfoGet(BaseModel):
    fix_info_id: int
    car_id: int
    mechanic_id: int
    fix_date: datetime
    work_type: str
    destroy_degree: float
    work_duration: int


class SFixInfoAdd(BaseModel):
    car_id: int = Field(..., description='Car id')
    mechanic_id: int = Field(..., description='Mechanic id')
    fix_date: datetime = Field(..., description='Fix date')
    work_type: str = Field(..., description='Work type')
    destroy_degree: float = Field(..., description='Destroy degree')
    work_duration: int = Field(..., description='Work duration')


    @classmethod
    @field_validator('fix_date')
    def validate_fix_date(cls, fix_date: datetime):
        if fix_date > datetime.now():
            raise ValueError('Fix date cannot be in the future')

        return fix_date


    @classmethod
    @field_validator('work_duration')
    def validate_age(cls, work_duration: int):
        if work_duration < 0:
            raise ValueError('Driver time accidents must be positive.')

        return work_duration


class SFixInfoUpdate(BaseModel):
    fix_date: datetime | None = Field(None, description='Fix date')
    work_type: str | None = Field(None, description='Work type')
    destroy_degree: float | None = Field(None, description='Destroy degree')
    work_duration: int | None = Field(None, description='Work duration')


    @classmethod
    @field_validator('fix_date')
    def validate_fix_date(cls, fix_date: datetime):
        if fix_date and fix_date > datetime.now():
            raise ValueError('Fix date cannot be in the future')

        return fix_date


    @classmethod
    @field_validator('work_duration')
    def validate_age(cls, work_duration: int):
        if work_duration and work_duration < 0:
            raise ValueError('Driver time accidents must be positive.')

        return work_duration
