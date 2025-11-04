"""
Модуль моделей приложения.

Содержит импорт всех моделей базы данных для удобного доступа извне.
Позволяет импортировать модели напрямую из пакета app.models вместо указания
полного пути.
"""

from .charity_project import CharityProject # noqa
from .donation import Donation # noqa
from .user import User # noqa
