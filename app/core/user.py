from typing import Optional, Union, AsyncGenerator

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate
from app.service.constants import MIN_PASSWORD_LENGTH, TOKEN_LIFETIME


async def get_user_db(session: AsyncSession = Depends(get_async_session)
                      ) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """Возвращает экземпляр базы данных пользователей SQLAlchemy."""
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Возвращает стратегию JWT с заданным секретом и временем жизни."""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=TOKEN_LIFETIME)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер пользователей с валидацией пароля и обработкой регистрации."""

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Проверяет пароль на соответствие требованиям.

        Args:
            password: Пароль для проверки
            user: Пользователь или схема создания пользователя

        Raises:
            InvalidPasswordException: Если пароль слишком короткий или
            содержит email
        """
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordException(
                reason=(
                    'Пароль не должен быть короче'
                    f' {MIN_PASSWORD_LENGTH} символов.'
                )
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не должен содержать e=mail.'
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ) -> None:
        """Отправляет приветственное письмо после успешной регистрации.

        Args:
            user: Зарегистрированный пользователь
            request: Необязательный объект запроса
        """
        await self.send_welcome_email(user.email)

    async def send_welcome_email(self, email: str) -> None:
        """Отправляет приветственное письмо на указанный email."""


async def get_user_manager(user_db=Depends(get_user_db)
                           ) -> AsyncGenerator[UserManager, None]:
    """Возвращает менеджер пользователей для dependency injection."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
