from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, Boolean

from app.core.db import Base
from app.service.constants import DEFAULT_INVESTED_AMOUNT


def get_utc_now() -> datetime:
    """Возвращает текущее время в UTC с учетом временной зоны."""
    return datetime.now(timezone.utc)


class CustomBaseModel(Base):
    """Абстрактная  модель с общими полями для проектов и пожертвований.

    Используется при наследовании моделями CharityProject и Donation.
    """

    __abstract__ = True

    full_amount: int = Column(
        Integer,
        nullable=False,
        comment='Полная сумма, требуемая для проекта или пожертвованная'
    )
    invested_amount: int = Column(
        Integer,
        default=DEFAULT_INVESTED_AMOUNT,
        comment='Сумма, уже распределенная по проектам'
    )
    fully_invested: bool = Column(
        Boolean,
        default=False,
        comment='Метка, показывающая, что все средства были распределены'
    )
    create_date: datetime = Column(
        DateTime,
        default=get_utc_now,
        comment='Дата и время создания записи'
    )
    close_date: datetime = Column(
        DateTime,
        comment='Дата завершения распределения средств'
    )
