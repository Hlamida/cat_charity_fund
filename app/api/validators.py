from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DEFAULT_ZERO
from app.crud.charity_project import charity_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверяет наличие дубликата проекта."""

    proj_id = await charity_crud.get_project_id_by_name(
        project_name,
        session,
    )
    if proj_id is not None:

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_before_edit(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверяет наличие проекта по id."""

    project = await charity_crud.get(
        obj_id=project_id,
        session=session,
    )
    if not project:

        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!',
        )

    return project


async def check_project_closed(
        project_id: int,
        session: AsyncSession,
) -> None:
    """Проверяет, закрыт ли проект."""

    project = await charity_crud.get(
        obj_id=project_id,
        session=session,
    )
    if project.fully_invested:

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )


async def check_donations_poured(
        project_id: int,
        session: AsyncSession,
) -> None:
    """Проверяет наличие инвестиций в проект."""

    project = await charity_crud.get(
        obj_id=project_id,
        session=session,
    )
    if project.invested_amount > DEFAULT_ZERO:

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_new_sum_less_invested(
        new_sum: int,
        project_id: int,
        session: AsyncSession,
) -> None:
    """Сравнивает новую сумму с инвестированной."""

    project = await charity_crud.get(
        obj_id=project_id,
        session=session,
    )
    if new_sum < project.invested_amount:

        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить сумму меньше инвестированной!',
        )
