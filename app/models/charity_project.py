from sqlalchemy import Column, String, Text

from app.constants import (MAX_CHARITY_PROJECT_NAME_LENGTH,
                           MAX_DESCRIPTION_PREV_LEN)
from app.models.base import CharityBaseModel


class CharityProject(CharityBaseModel):
    name = Column(
                 String(MAX_CHARITY_PROJECT_NAME_LENGTH),
                 unique=True, nullable=False
    )
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (f'{self.name}({self.description[:MAX_DESCRIPTION_PREV_LEN]})'
                f'{super().__repr__()}')
