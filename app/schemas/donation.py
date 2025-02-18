from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, validator


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt


class DonationCreate(DonationBase):

    @validator('full_amount')
    def full_amount_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Пожертвование не может быть пустым!')
        return value

    @validator('comment')
    def comment_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Комментарий не может быть пустым!')
        return value


class DonationMe(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationMe):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime

    class Config:
        orm_mode = True