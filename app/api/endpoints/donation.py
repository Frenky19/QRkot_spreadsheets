from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User, CharityProject
from app.schemas.donation import DonationCreate, DonationDB, DonationAdminDB
from app.service.donations import invest_funds

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationAdminDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> List[DonationAdminDB]:
    """Получает список всех пожертвований.

    Доступно только для суперпользователей.

    Args:
        session: Асинхронная сессия для работы с базой данных

    Returns:
        list[DonationAdminDB]: Список всех пожертвований с дополнительной
                                информацией
    """
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> DonationDB:
    """Создает новое пожертвование.

    Args:
        donation: Данные для создания пожертвования
        session: Асинхронная сессия для работы с базой данных
        user: Текущий аутентифицированный пользователь

    Returns:
        DonationDB: Созданное пожертвование
    """
    new_donation = await donation_crud.create(
        donation, session, user, commit=False
    )
    projects = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested.is_(False)
    ).order_by(CharityProject.create_date))
    projects = projects.scalars().all()
    modified_objects = invest_funds(new_donation, projects)
    session.add_all(modified_objects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> List[DonationDB]:
    """Получает список пожертвований текущего пользователя.

    Args:
        session: Асинхронная сессия для работы с базой данных
        user: Текущий аутентифицированный пользователь

    Returns:
        list[DonationDB]: Список пожертвований пользователя
    """
    return await donation_crud.get_by_user(session, user)
