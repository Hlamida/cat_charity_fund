from typing import Generic, Optional, List, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase(Generic[ModelType]):
    """Базовый класс для операций с БД."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_multi(
            self,
            session: AsyncSession,
    ) -> List[ModelType]:
        """Возвращает все запрошенные экземпляры."""

        db_objs = await session.execute(select(self.model))

        return db_objs.scalars().all()

    async def get_multi_open(
            self,
            session: AsyncSession,
    ) -> List[ModelType]:
        """Возвращает все незавершённые экземпляры."""

        db_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            ).order_by('create_date')
        )

        return db_objs.scalars().all()
