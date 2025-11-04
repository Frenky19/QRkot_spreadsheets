"""Модуль маршрутизаторов API приложения.

Содержит импорт всех роутеров API для удобного доступа извне.
Позволяет импортировать роутеры напрямую из пакета app.api.endpoints
вместо указания полного пути к каждому модулю.
"""

from .charity_project import router as charity_project_router # noqa
from .donation import router as donation_router # noqa
from .google import router as google_router # noqa
from .user import router as user_router # noqa
