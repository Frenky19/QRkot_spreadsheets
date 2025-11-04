from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.service.constants import (MAX_PROJECT_NAME_LENGTH,
                                   MIN_INVESTED_AMOUNT,
                                   MIN_DESCRIPTION_LENGTH,
                                   MIN_PROJECT_NAME_LENGTH)


class CharityProjectBase(BaseModel):
    """Базовая схема благотворительного проекта.

    Используется при наследовании схемами CharityProjectCreate,
    CharityProjectUpdate, CharityProjectDB.
    """

    name: str = Field(
        ...,
        min_length=MIN_PROJECT_NAME_LENGTH,
        max_length=MAX_PROJECT_NAME_LENGTH,
        description='Название проекта'
    )
    description: str = Field(
        ...,
        min_length=MIN_DESCRIPTION_LENGTH,
        description='Описание проекта'
    )
    full_amount: int = Field(
        ...,
        gt=MIN_INVESTED_AMOUNT,
        description='Требуемая сумма для проекта'
    )

    class Config:
        schema_extra = {
            'example': {
                'name': 'Поддержка котиков в их стремлениях',
                'description': 'Сбор средств на покупку елок',
                'full_amount': 100000
            }
        }


class CharityProjectCreate(CharityProjectBase):
    """Создание нового благотворительного проекта."""


class CharityProjectUpdate(CharityProjectBase):
    """Обновление данных существующего благотворительного проекта."""

    name: Optional[str] = Field(
        None,
        min_length=MIN_PROJECT_NAME_LENGTH,
        max_length=MAX_PROJECT_NAME_LENGTH,
        description='Название проекта'
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_DESCRIPTION_LENGTH,
        description='Описание проекта'
    )
    full_amount: Optional[int] = Field(
        None,
        gt=0,
        description='Требуемая сумма для проекта'
    )

    class Config:
        schema_extra = {
            'example': {
                'name': 'Новое название проекта',
                'description': 'Обновленное описание',
                'full_amount': 10000
            }
        }


class CharityProjectDB(CharityProjectBase):
    """Возвращает данные о проекте из БД."""

    id: int = Field(..., description='Уникальный идентификатор проекта')
    invested_amount: int = Field(0, description='Сумма уже внесенных средств')
    fully_invested: bool = Field(
        False,
        description='Отметка о завершении сбора средств'
    )
    create_date: datetime = Field(..., description='Дата создания проекта')
    close_date: Optional[datetime] = Field(
        None,
        description='Дата закрытия проекта'
    )

    class Config:
        orm_mode = True


class CharityProjectReport(BaseModel):
    """Схема для отчёта по закрытым проектам."""

    name: str
    collection_time: str
    description: str
    collected_amount: int
    close_date: str

    class Config:
        orm_mode = True
