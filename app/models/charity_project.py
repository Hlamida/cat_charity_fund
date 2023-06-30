from sqlalchemy import Column, String, Text

from app.core.constants import MAX_STRING_LENGTH
from app.models.base import CharityBase


class CharityProject(CharityBase):
    name = Column(
        String(MAX_STRING_LENGTH), unique=True, nullable=False,
    )
    description = Column(Text, nullable=False)

    def __repr__(self):
        remains_amount = self.full_amount - self.invested_amount
        return (
            f'{self.name}. Осталось собрать: {remains_amount} руб.'
        )
