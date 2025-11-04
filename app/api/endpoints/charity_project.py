from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.service.constants import MIN_INVESTED_AMOUNT
from app.service.donations import invest_funds


router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    """Получает список всех благотворительных проектов.

    Args:
        session: Асинхронная сессия для работы с базой данных

    Returns:
        list[CharityProjectDB]: Список всех благотворительных проектов
    """
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Создает новый благотворительный проект.

    Доступно только для суперпользователей.

    Args:
        project: Данные для создания проекта
        session: Асинхронная сессия для работы с базой данных

    Returns:
        CharityProjectDB: Созданный благотворительный проект

    Raises:
        HTTPException: Если проект с таким именем уже существует
    """
    project_id = await charity_project_crud.get_project_id_by_name(
        project.name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )
    new_project = await charity_project_crud.create(
        project, session, commit=False
    )
    donations = await session.execute(select(Donation).where(
        Donation.fully_invested.is_(False)
    ).order_by(Donation.create_date))
    donations = donations.scalars().all()
    modified_objects = invest_funds(new_project, donations)
    for obj in modified_objects:
        session.add(obj)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Удаляет благотворительный проект.

    Доступно только для суперпользователей.

    Args:
        project_id: ID проекта для удаления
        session: Асинхронная сессия для работы с базой данных

    Returns:
        CharityProjectDB: Удаленный благотворительный проект

    Raises:
        HTTPException: Если проект не найден или в него уже внесены средства
    """
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Проект не найден')
    if project.invested_amount > MIN_INVESTED_AMOUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    project = await charity_project_crud.remove(project, session)
    await session.commit()
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Обновляет данные благотворительного проекта.

    Доступно только для суперпользователей.

    Args:
        project_id: ID проекта для обновления
        obj_in: Данные для обновления проекта
        session: Асинхронная сессия для работы с базой данных

    Returns:
        CharityProjectDB: Обновленный благотворительный проект

    Raises:
        HTTPException: Если проект не найден, закрыт или данные невалидны
    """
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден'
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    update_data = obj_in.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Не указаны поля для обновления'
        )
    if obj_in.name is not None:
        existing_project = await charity_project_crud.get_project_id_by_name(
            obj_in.name, session)
        if existing_project is not None and existing_project != project_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Проект с таким именем уже существует!'
            )
    if (obj_in.full_amount is not None and
            obj_in.full_amount < project.invested_amount):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Нельзя установить значение full_amount '
                    'меньше уже вложенной суммы.')
        )
    project = await charity_project_crud.update(project, obj_in, session)
    await session.commit()
    await session.refresh(project)
    return project
