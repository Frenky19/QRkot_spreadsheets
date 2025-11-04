"""Экземпляр настроек приложения для использования во всем проекте."""

from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Настройки приложения, загружаемые из переменных окружения."""

    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Позволяет поддержать котиков в их начинаниях'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: str = 'https://accounts.google.com/o/oauth2/auth'
    token_uri: str = 'https://oauth2.googleapis.com/token'
    auth_provider_x509_cert_url: str = (
        'https://www.googleapis.com/oauth2/v1/certs'
    )
    client_x509_cert_url: Optional[str] = None
    email: Optional[EmailStr] = None
    spreadsheet_id: Optional[str] = None

    class Config:
        """Конфигурация для загрузки переменных окружения из файла."""
        env_file = '.env'


settings = Settings()
