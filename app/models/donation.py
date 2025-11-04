from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import CustomBaseModel
from app.models.user import User


class Donation(CustomBaseModel):
    """Модель пожертвований для проектов.

    Наследует общие поля из CustomBaseModel
    (сумма, статус инвестирования, даты).
    Связана с моделью User через внешний ключ user_id.
    """

    user_id: int = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False,
        comment='ID пользователя, сделавшего пожертвование'
    )
    comment: str = Column(
        String,
        comment='Комментарий к пожертвованию'
    )
    user = relationship(
        User,
        backref='donations'
    )
