from datetime import timedelta
from typing import Optional
from operator import itemgetter

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectReport
from app.service.constants import (
    SECONDS_IN_HOUR,
    SECONDS_IN_MINUTE,
)


class CRUDCharityProject(CRUDBase):
    """CRUD-операции для модели CharityProject."""

    async def get_project_id_by_name(
        self, project_name: str, session: AsyncSession
    ) -> Optional[int]:
        """Получает ID благотворительного проекта по его названию.

        Args:
            project_name: Название проекта для поиска
            session: Асинхронная сессия базы данных

        Returns:
            Optional[int]: ID проекта если найден, иначе None
        """
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[CharityProjectReport]:
        """Получает закрытые проекты, отсортированные по скорости закрытия."""
        stmt = select(CharityProject).where(
            CharityProject.fully_invested.is_(True)
        )
        db_projects = await session.execute(stmt)
        projects = db_projects.scalars().all()
        projects_with_time = []
        for project in projects:
            if project.close_date and project.create_date:
                time_diff = project.close_date - project.create_date
                collection_time = self._format_time_delta(time_diff)
                close_date_str = project.close_date.strftime('%Y-%m-%d %H:%M')
                projects_with_time.append({
                    'project': project,
                    'collection_time': collection_time,
                    'close_date_str': close_date_str,
                    'time_seconds': time_diff.total_seconds()
                })
        projects_with_time.sort(key=itemgetter('time_seconds'))
        report_projects = []
        for item in projects_with_time:
            project = item['project']
            report_projects.append(
                CharityProjectReport(
                    name=project.name,
                    collection_time=item['collection_time'],
                    description=project.description,
                    collected_amount=project.invested_amount,
                    close_date=item['close_date_str']
                )
            )
        return report_projects

    def _format_time_delta(self, td: timedelta) -> str:
        """Форматирует timedelta в читаемый вид."""
        days = td.days
        hours, remainder = divmod(td.seconds, SECONDS_IN_HOUR)
        minutes, seconds = divmod(remainder, SECONDS_IN_MINUTE)
        if days > 0:
            return f'{days} дн. {hours:02} ч. {minutes:02} мин.'
        elif hours > 0:
            return f'{hours} ч. {minutes:02} мин.'
        else:
            return f'{minutes} мин. {seconds:02} сек.'


charity_project_crud = CRUDCharityProject(CharityProject)
