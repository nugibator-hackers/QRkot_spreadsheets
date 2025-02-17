from sqlalchemy import Column, ForeignKey, Integer, Text

from app.constants import MAX_DESCRIPTION_PREV_LEN
from app.models.base import CharityBaseModel


class Donation(CharityBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (f'User {self.user_id}'
                f'({self.comment[:MAX_DESCRIPTION_PREV_LEN]})'
                f'{super().__repr__()}')
