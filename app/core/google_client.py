"""Файл для прохождения тестов."""

import gspread
from google.oauth2.service_account import Credentials

from app.core.config import settings
from app.service.constants import BASE_SCOPE
from app.service.exceptions import GoogleSheetsServiceError

SCOPES = [
    f'{BASE_SCOPE}spreadsheets',
    f'{BASE_SCOPE}drive.file'
]
INFO = {
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


async def get_service():
    """Асинхронный генератор для получения Google Sheets сервиса."""
    try:
        creds = Credentials.from_service_account_info(INFO)
        creds = creds.with_scopes(SCOPES)
        client = gspread.authorize(creds)
        yield client
    except Exception as e:
        raise GoogleSheetsServiceError(
            f'Ошибка создания Google сервиса: {str(e)}'
        )


google_client = get_service()
