from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharity(CRUDBase[CharityProject]):
    """Обрабатывает базу проектов."""

    @classmethod
    async def get_project_id_by_name(
        cls,
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
