from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Название проекта не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Описание проекта не может быть пустым!')
        if value == '':
            raise ValueError('Поле ОПИСАНИЕ должно содержать'
                             'хотя бы один символ!')
        return value

    @validator('full_amount')
    def full_amount_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Требуемая сумма не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    full_amount: PositiveInt
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime

    class Config:
        orm_mode = True