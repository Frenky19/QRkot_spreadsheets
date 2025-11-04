from http import HTTPStatus

import gspread
import logging
from google.oauth2.service_account import Credentials
from fastapi import HTTPException
from typing import Optional

from app.core.config import settings
from app.schemas.charity_project import CharityProjectReport
from app.service.constants import (
    SPREADSHEET_HEADERS,
    SPREADSHEET_COLUMN_COUNT,
    SPREADSHEET_HEADER_RANGE,
    SPREADSHEET_HEADER_BACKGROUND
)

logger = logging.getLogger(__name__)


class GoogleAPIService:
    """Сервис для работы с Google Sheets API."""

    def __init__(self):
        try:
            self.credentials = self._get_credentials()
            self.client = gspread.authorize(self.credentials)
            logger.info('Google API client инициализирован успешно')
        except Exception as e:
            logger.error(f'Ошибка инициализации Google API: {str(e)}')
            raise

    def _get_credentials(self) -> Credentials:
        """Получает учетные данные для доступа к Google API."""
        try:
            logger.info('Получение credentials...')
            required_fields = ['type', 'project_id', 'private_key_id',
                               'private_key', 'client_email']
            for field in required_fields:
                if not getattr(settings, field, None):
                    raise ValueError(f'Отсутствует обязательное поле: {field}')
            creds_dict = {
                'type': settings.type,
                'project_id': settings.project_id,
                'private_key_id': settings.private_key_id,
                'private_key': settings.private_key.replace('\\n', '\n'),
                'client_email': settings.client_email,
                'client_id': settings.client_id,
                'auth_uri': settings.auth_uri,
                'token_uri': settings.token_uri,
                'auth_provider_x509_cert_url': (
                    settings.auth_provider_x509_cert_url
                ),
                'client_x509_cert_url': settings.client_x509_cert_url,
            }
            logger.info('Credentials созданы, аутентификация...')
            SCOPES = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file'
            ]
            creds = Credentials.from_service_account_info(creds_dict)
            creds = creds.with_scopes(SCOPES)
            return creds
        except Exception as error:
            logger.error(f'Ошибка аутентификации: {str(error)}')
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f'Ошибка аутентификации в Google API: {str(error)}'
            )

    def update_spreadsheet(
        self,
        projects: list[CharityProjectReport],
        spreadsheet_id: Optional[str] = None
    ) -> str:
        """Обновляет данные в существующей таблице."""
        try:
            target_spreadsheet_id = spreadsheet_id or settings.spreadsheet_id
            if not target_spreadsheet_id:
                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail='Не указан ID таблицы. Укажите SPREADSHEET_ID'
                )
            logger.info(f'Открываем таблицу с ID: {target_spreadsheet_id}')
            spreadsheet = self.client.open_by_key(target_spreadsheet_id)
            worksheet = spreadsheet.sheet1
            worksheet.clear()
            worksheet.update(SPREADSHEET_HEADER_RANGE, [SPREADSHEET_HEADERS])
            data = []
            for project in projects:
                data.append([
                    project.name,
                    project.collection_time,
                    project.description,
                    project.collected_amount,
                    project.close_date
                ])
            if data:
                worksheet.update(f'A2:E{len(data) + 1}', data)
            worksheet.format(SPREADSHEET_HEADER_RANGE, {
                'textFormat': {'bold': True},
                'backgroundColor': SPREADSHEET_HEADER_BACKGROUND
            })
            try:
                worksheet.columns_auto_resize(0, SPREADSHEET_COLUMN_COUNT)
            except Exception as e:
                logger.warning(
                    f'Не удалось автоматически изменить размер колонок: {e}'
                )
            logger.info(f'Таблица обновлена {len(data)} проектами')
            return spreadsheet.url
        except gspread.SpreadsheetNotFound:
            logger.error(f'Таблица с ID {target_spreadsheet_id} не найдена')
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=(
                    'Таблица не найдена. '
                    'Проверьте SPREADSHEET_ID и права доступа'
                )
            )
        except Exception as error:
            logger.error(f'Ошибка обновления таблицы: {str(error)}')
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f'Ошибка обновления таблицы: {str(error)}'
            )


google_api_service = GoogleAPIService()