"""Главный роутер приложения, объединяющий все эндпоинты API.

Этот модуль создает основной маршрутизатор и включает в него все дочерние
роутеры для обработки запросов к различным ресурсам приложения.
"""

from fastapi import APIRouter

from app.api.endpoints import (charity_project_router, donation_router,
                               google_router, user_router)


main_router = APIRouter()

main_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['charity_projects']
)
main_router.include_router(
    donation_router, prefix='/donation', tags=['donations']
)
main_router.include_router(user_router)
main_router.include_router(
    google_router, prefix='/google', tags=['Google']
)
