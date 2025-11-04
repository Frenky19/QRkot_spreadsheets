from sqlalchemy import Column, String

from app.models.base import CustomBaseModel
from app.service.constants import MAX_PROJECT_NAME_LENGTH


class CharityProject(CustomBaseModel):
    """Модель благотворительного проекта для котиков.

    Наследует общие поля из CustomBaseModel
    (сумма, статус инвестирования, даты).
    Представляет конкретный благотворительный проект,
    который нуждается в финансировании.
    """

    name: str = Column(
        String(MAX_PROJECT_NAME_LENGTH),
        unique=True,
        nullable=False,
        comment='Уникальное название благотворительного проекта'
    )
    description: str = Column(
        String,
        nullable=False,
        comment='Подробное описание проекта и его целей'
    )
