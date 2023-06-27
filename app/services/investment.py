from datetime import datetime
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.crud.base import CRUDBase

ModelType = TypeVar('ModelType', bound=Base)
CRUDType = TypeVar('CRUDType', bound=CRUDBase)


def close_investment(obj: ModelType) -> None:
    """Проставляет атрибуты закрытой позиции."""

    obj.fully_invested = True
    obj.close_date = datetime.now()


async def investment(
    invest_from: ModelType, invest_to: CRUDType, session: AsyncSession
) -> ModelType:
    """Инвестирует при создании нового объекта"""

    objects = await invest_to.get_multi_open(session)
    for object in objects:
        for_invest = invest_from.full_amount - invest_from.invested_amount
        investitions = object.full_amount - object.invested_amount
        to_invest = min(for_invest, investitions)
        object.invested_amount += to_invest
        invest_from.invested_amount += to_invest
        if object.full_amount == object.invested_amount:
            close_investment(object)
        if invest_from.full_amount == invest_from.invested_amount:
            close_investment(invest_from)
            break
    session.add_all((*objects, invest_from))
    await session.commit()
    await session.refresh(invest_from)
    return invest_from
