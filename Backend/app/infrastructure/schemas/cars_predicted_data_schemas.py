from pydantic import (
    BaseModel,
    Field,
)


class SCarPredictedDataGet(BaseModel):
    car_id: int
    target_reg: float
    target_class: str


class SCarPredictedDataAdd(BaseModel):
    car_id: int = Field(..., description='Car id')
    target_reg: float = Field(..., description='Target reg')
    target_class: str = Field(..., description='Target class')


class SCarPredictedDataUpdate(BaseModel):
    target_reg: float | None = Field(None, description='Target reg')
    target_class: str | None = Field(None, description='Target class')

