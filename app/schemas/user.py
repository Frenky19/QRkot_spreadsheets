from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Чтение данных пользователя."""


class UserCreate(schemas.BaseUserCreate):
    """Создание пользователя."""


class UserUpdate(schemas.BaseUserUpdate):
    """Обновление данных пользователя."""
