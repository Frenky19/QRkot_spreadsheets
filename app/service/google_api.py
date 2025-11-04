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
                "type": "service_account",
                "project_id": "qrkot-477119",
                "private_key_id": "6512ffee0d4a7f743fdf5a660ac0be7600f68b1b",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDddOwOVjDkTsQX\n70FuNIuReh99fkWQ13nJzB8cipuChYgTg5Fny3mSirmQ+GiwLTCADDoXizXnceqs\nuC0UArhpuP/+AUhgUdr63a4HxxPwYLsp/3xFp+04zqk1dNrIrVFItTXzy6AlMLww\nOPki7qTwuafp3ooACJl68NCP+u/dkWsmO6Qhfn7Iqdk9AXa83bjpaLx/GQNGj+yJ\nh0010A/GwmmUFG9eWmTK5avsQ9Qk6cZIIompPI7/dnY7cuCUtAfLAFyIJ+hcfmNc\nm3ZFvp3lA8d2Ia/NTvrLbinz2rNMKXu0izPElhfbmBrysoWIR+ubvJM917mDx2Ej\ne6C7HkANAgMBAAECggEAG2M/YlKEf2fCVpdvRxrWe+pXhKSeI9iSJkPJQTVfIBg1\niPxHekeuxFHFu0kNYWRlUCCy+oBr7TCobi3k3Ums1t5bQmWUNt1IsKfDwxB6xcqg\nuwPusYqgCtt8D7Fg8VqF5/EJOBphtte9HlWdchWDboX3XzP3ayOlH5AyquvEyGjd\nqkvFqPi88wzdst6fEWGYxihQBxXEr1sIqHszqi4tKRll9+Fu0nQqq4vXJG6JYeHJ\nr90kWpc1R01UrBLOktzCAQe8IsqINE2pW3zn4I8R6fABTSgacqFfLvMsSEnoZJsd\n+IUFq5FIfoqLAmKpNpYbHVw0ODvCYuQdQMFnYZxqwQKBgQDxcTSEEimT6kpo+ILL\n+z77bXQo1FDl877u6A23OdRmJSH076h0hsuYUy78J1jPqAXr3P9k/5OhssuHgx+k\n48m7ftfcjsEQlaA4lBy/aqzXXROLdanGMWfPLNHMRbuwwjnpQtKNOg1H+VDFMU3s\ng1379ZoyqImONdA3kuxgdsiW0QKBgQDqzzrdE0Rurm6TbjWEYUN0Dkm5rvUZd1aI\nlyajTSGN7BZs1PS4/W3Z5ofjBhbE7LqNlQZkwg7DNijdTb2fw6KKRlrPbTRWgLiH\nKnb23WB4tEl0qTd1ink6M67N86qQf8fh7LcYzHRn6QFTAoA/Z0rZhkEnnvCHxCRz\nirojxsHcfQKBgQCL3nb748GubNX6hazQGpbb9QaL+KN8832yzT/U222OVwia6pN+\nHfCoJ9haPzkV41K61uYlTmHqFLgPowib71IYilzm6tQxlVyiKjuVMGk8wjDmY52c\nsVZgEKjhW6xls770wL9VDUJQZcBC3FM2Jsw1gIx5uGUnu0kKSNUi9O0zYQKBgFxE\n7JOdE6IOp2MFxr/rXI9JYg02RBgqvfVUuBkpoQrc//7qO/RJmhYrMbCzXtUpVTF3\noxiK7TQmny4/c0lJniCJ/vtNpWhskpaCyFa/rT4hUlAmgqWMsZB+aK2Dl73KiKgt\n1dFH3mJKvHt7GxxPIamSyR2hplEjcVN56yVN4DYdAoGABIfE67SqJ9lRC/5MkAb+\na3Tp87D5h5MvzgrWklG9/30XAtrqy7jTLbFOKtAeuLriHK2S33OeJ6xHjaBXuyDL\n0FbnrMNVYSGn/chCpE+T04LDebduFUhiUz4bDRKUVCqNR/V+jKujHuh+zse17cUE\nmK4alCn2MfGSQ33sxPsrSz8=\n-----END PRIVATE KEY-----\n",  # noqa
                'client_email': "qrkot-service-account@qrkot-477119.iam.gserviceaccount.com",  # noqa
                'client_id': "111680164008296313353",
                'auth_uri': "https://accounts.google.com/o/oauth2/auth",
                'token_uri': "https://oauth2.googleapis.com/token",
                'auth_provider_x509_cert_url': (
                    "https://www.googleapis.com/oauth2/v1/certs",
                ),
                'client_x509_cert_url': "https://www.googleapis.com/robot/v1/metadata/x509/qrkot-service-account%40qrkot-477119.iam.gserviceaccount.com",  # noqa
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