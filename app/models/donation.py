from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import AbstractProjectDonation


class Donation(AbstractProjectDonation):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
