from sqlalchemy import Column, String, Text

from app.core.constant import MAX_NAME_LENGTH
from app.models.base import BaseModel


class CharityProject(BaseModel):
    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
