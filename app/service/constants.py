"""Модуль констант приложения.

Содержит все основные константы, используемые в различных частях приложения.
Константы сгруппированы по функциональному назначению для удобства
использования и поддержки.

TOKEN_LIFETIME: Время жизни JWT-токена в секундах (1 час).

MIN_PASSWORD_LENGTH: Минимальная допустимая длина пароля пользователя.

MIN_INVESTED_AMOUNT: Минимально допустимая сумма инвестиций в проект.

DEFAULT_INVESTED_AMOUNT: Значение инвестированной суммы по умолчанию при
                        создании проекта.

MAX_PROJECT_NAME_LENGTH: Максимальная допустимая длина названия
                        благотворительного проекта.

MIN_PROJECT_NAME_LENGTH: Минимальная допустимая длина названия
                        благотворительного проекта.

MIN_DESCRIPTION_LENGTH: Минимальная допустимая длина описания
                        благотворительного проекта.

SPREADSHEET_HEADERS: Заголовки колонок для отчета в Google Таблицах.

SPREADSHEET_COLUMN_COUNT: Количество колонок в отчете Google Таблиц.

SPREADSHEET_HEADER_RANGE: Диапазон ячеек для заголовков отчета.

SPREADSHEET_HEADER_BACKGROUND: Цвет фона для заголовков отчета.

SECONDS_IN_HOUR: Количество секунд в одном часе.

SECONDS_IN_MINUTE: Количество секунд в одной минуте.
"""

# Аутентификация и пользователи
TOKEN_LIFETIME = 3600
MIN_PASSWORD_LENGTH = 3

# Проекты
MAX_PROJECT_NAME_LENGTH = 100
MIN_PROJECT_NAME_LENGTH = 1
MIN_DESCRIPTION_LENGTH = 1
MIN_INVESTED_AMOUNT = 0
DEFAULT_INVESTED_AMOUNT = 0

# Google Sheets
SPREADSHEET_HEADERS = [
    'Название проекта',
    'Время сбора',
    'Описание',
    'Собрано средств',
    'Дата закрытия'
]
SPREADSHEET_COLUMN_COUNT = 4
SPREADSHEET_HEADER_RANGE = 'A1:E1'
SPREADSHEET_HEADER_BACKGROUND = {
    'red': 0.9,
    'green': 0.9,
    'blue': 0.9
}
BASE_SCOPE = 'https://www.googleapis.com/auth/'

# Форматирование времени
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60
