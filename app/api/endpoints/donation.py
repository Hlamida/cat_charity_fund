from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.charity_project import charity_crud
from app.crud.donation import donations_crud
from app.models import User
from app.services.investment import investment
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationDBFull,
)


router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDBFull],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех пожертвований. Только для superuser."""

    donations = await donations_crud.get_multi(session)

    return donations


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Возвращает пожертвования зарегистрированного пользователя."""

    donations = await donations_crud.get_by_user(user, session)

    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def create_new_donation(
        project: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Создаёт новое пожертвование для зарегистрированного пользователя."""

    donation = await donations_crud.create(project, session, user)
    await investment(donation, charity_crud, session)

    return donation
