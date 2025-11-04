from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser


app = FastAPI(title=settings.app_title, description=settings.app_description)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    """Функция, выполняемая при запуске приложения.

    Создает первого суперпользователя в системе, если он еще не существует.
    Использует настройки из конфигурации приложения.
    """
    await create_first_superuser()
