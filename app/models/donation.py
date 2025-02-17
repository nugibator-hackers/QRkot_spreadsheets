from sqlalchemy import Column, ForeignKey, Integer, Text

from app.constants import MAX_DESCRIPTION_PREVIEW_LENGTH
from app.models.base import CharityBaseModel


class Donation(CharityBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (f'User {self.user_id}({self.comment[:MAX_DESCRIPTION_PREVIEW_LENGTH]})'
                f'{super().__repr__()}')
