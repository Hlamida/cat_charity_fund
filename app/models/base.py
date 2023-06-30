from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.constants import DEFAULT_ZERO
from app.core.db import Base


class CharityBase(Base):

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_ZERO)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None, nullable=True)
