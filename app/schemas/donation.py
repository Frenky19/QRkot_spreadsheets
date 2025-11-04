from datetime import datetime

from pydantic import BaseModel, Field

from app.service.constants import MIN_INVESTED_AMOUNT


class DonationBase(BaseModel):
    """Базовая схема пожертвования.

    Используется при наследовании схемами DonationCreate и
    DonationDB.
    """

    full_amount: int = Field(
        ..., gt=MIN_INVESTED_AMOUNT, description='Сумма пожертвования'
    )
    comment: str = Field(None, description='Комментарий к пожертвованию')

    class Config:
        schema_extra = {
            'example': {
                'full_amount': 5000,
                'comment': 'Для пушистых',
            }
        }


class DonationCreate(DonationBase):
    """Создание нового пожертвования."""


class DonationDB(DonationBase):
    """Возвращает данные о пожертвовании из БД.

    Используется при наследовании схемой DonationAdminDB.
    """

    id: int = Field(..., description='Уникальный идентификатор пожертвования')
    create_date: datetime = Field(
        ...,
        description='Дата создания пожертвования'
    )

    class Config:
        orm_mode = True


class DonationAdminDB(DonationDB):
    """Возвращает данные о пожертвовании из БД для админа."""

    user_id: int = Field(
        ...,
        description='ID пользователя, сделавшего пожертвование'
    )
    invested_amount: int = Field(
        0,
        description='Сумма, уже распределенная по проектам'
    )
    fully_invested: bool = Field(
        False,
        description='Флаг полного распределения средств'
    )
    close_date: datetime = Field(
        None,
        description='Дата полного распределения средств'
    )
