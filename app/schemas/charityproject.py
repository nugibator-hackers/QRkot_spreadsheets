from typing import Optional

from datetime import datetime

from app.core.constant import (DEFAULT_INVESTED_AMOUNT,
                               DEFAULT_FULLY_INVESTED,
                               MIN_NAME_LENGTH,
                               MAX_NAME_LENGTH,
                               MIN_DESCRIPTION_LENGTH)
from pydantic import Field, NonNegativeInt, StrictBool, BaseModel, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(..., min_length=MIN_NAME_LENGTH,
                                max_length=MAX_NAME_LENGTH)
    description: Optional[str]
    full_amount: NonNegativeInt


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=MIN_NAME_LENGTH,
                      max_length=MAX_NAME_LENGTH)
    description: str = Field(..., min_length=MIN_DESCRIPTION_LENGTH)

    @validator('full_amount')
    def check_full_amount(cls, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError(
                'сумма пожертвования должна быть целочисленной и больше 0')
        return value


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[NonNegativeInt]
    invested_amount: Optional[NonNegativeInt]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    fully_invested: Optional[StrictBool]

    @validator('name', allow_reuse=True)
    def name_cannot_be_null(cls, value):
        if value is None or value == '':
            raise ValueError('Имя может быть пустым')
        return value

    @validator('description', allow_reuse=True)
    def description_cannot_be_null(cls, value):
        if value is None or value == '':
            raise ValueError('Описание не может быть пустым')
        return value

    @validator('full_amount', allow_reuse=True)
    def full_amount_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Сумма не может быть пустой')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt = Field(...,
                                            example=DEFAULT_INVESTED_AMOUNT)
    fully_invested: StrictBool = Field(..., example=DEFAULT_FULLY_INVESTED)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
