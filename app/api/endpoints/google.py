from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.service.google_api import google_api_service


router = APIRouter()


@router.post(
    '/',
    response_model=dict,
    dependencies=[Depends(current_superuser)],
    summary='Обновить отчет в Google Таблице',
    description='Обновляет отчет с закрытыми проектами, '
                'отсортированными по скорости сбора средств'
)
async def update_google_report(
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Обновляет отчет в существующей Google Таблице."""
    try:
        projects = await charity_project_crud.get_projects_by_completion_rate(
            session
        )
        if not projects:
            return {
                'message': 'Нет закрытых проектов для отчета',
                'spreadsheet_url': None,
                'projects_count': 0
            }
        spreadsheet_url = google_api_service.update_spreadsheet(projects)
        return {
            'message': 'Отчет успешно обновлен',
            'spreadsheet_url': spreadsheet_url,
            'projects_count': len(projects)
        }
    except Exception as error:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при обновлении отчета: {str(error)}'
        )
