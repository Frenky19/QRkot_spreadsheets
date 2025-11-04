from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """CRUD-операции для модели Donation."""

    async def get_by_user(
        self, session: AsyncSession, user: User
    ) -> List[Donation]:
        """Получает все пожертвования, сделанные указанным пользователем.

        Args:
            session: Асинхронная сессия базы данных
            user: Пользователь, чьи пожертвования нужно получить

        Returns:
            List[Donation]: Список пожертвований пользователя
        """
        donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
