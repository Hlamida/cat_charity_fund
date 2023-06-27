from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectUpdate,
)


class CRUDCharity(CRUDBase[CharityProject]):
    """Обрабатывает базу проектов."""

    @staticmethod
    async def update(
            db_obj: CharityProject,
            obj_in: CharityProjectUpdate,
            session: AsyncSession,
    ) -> CharityProject:
        """Изменяет проект."""

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    @staticmethod
    async def remove(
            db_obj: CharityProject,
            session: AsyncSession,
    ) -> CharityProject:
        """Удаляет проект."""

        await session.delete(db_obj)
        await session.commit()

        return db_obj

    @staticmethod
    async def get_project_id_by_name(
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Возвращает проект по имени."""

        db_proj_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name,
            )
        )

        return db_proj_id.scalars().first()

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        """Возвращает проект."""

        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id,
            )
        )
        return db_obj.scalars().first()


charity_crud = CRUDCharity(CharityProject)
