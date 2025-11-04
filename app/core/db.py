from typing import AsyncGenerator

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Базовый класс для всех моделей, определяющий общие атрибуты."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Автоматически генерирует имя таблицы на основе имени класса.

        Returns:
            str: Имя таблицы в нижнем регистре
        """
        return cls.__name__.lower()

    id: int = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)
"""Базовый класс для объявления моделей с предустановленными атрибутами."""

engine = create_async_engine(settings.database_url)
"""Асинхронный движок для подключения к базе данных."""

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
"""Фабрика сессий для асинхронной работы с базой данных."""


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Генерирует асинхронную сессию для работы с базой данных.

    Yields:
        AsyncSession: Асинхронная сессия для работы с БД
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
