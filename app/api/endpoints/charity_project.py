from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_before_edit,
    check_new_sum_less_invested,
    check_donations_poured, check_project_closed,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.crud.donation import donations_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import investment


router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех проектов."""

    projects = await charity_crud.get_multi(session)

    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Добавляет новый проект. Только для superuser."""

    await check_name_duplicate(project.name, session)
    new_proj = await charity_crud.create(project, session)
    await investment(new_proj, donations_crud, session)

    return new_proj


@router.patch(
    '/{proj_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
        proj_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Изменяет проект по id. Только для superuser."""

    await check_project_closed(proj_id, session)
    if obj_in.full_amount:
        await check_new_sum_less_invested(obj_in.full_amount, proj_id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    project = await check_project_before_edit(
        proj_id,
        session,
    )
    project = await charity_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session,
    )
    await investment(project, donations_crud, session)

    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удаляет проект по id. Только для superuser."""

    project = await check_project_before_edit(
        project_id,
        session,
    )
    await check_donations_poured(project_id, session)
    project = await charity_crud.remove(project, session)

    return project
