from typing import Optional, Any, List, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


ModelType = TypeVar('ModelType')


class CRUDBase:
    """Базовый класс для CRUD-операций с моделями."""

    def __init__(self, model: Type[ModelType]):
        """Инициализирует CRUD-класс с указанной моделью.

        Args:
            model: SQLAlchemy модель для работы
        """
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        """Получает объект по его ID.

        Args:
            obj_id: ID объекта для поиска
            session: Асинхронная сессия базы данных

        Returns:
            Объект модели если найден, иначе None
        """
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[ModelType]:
        """Получает все объекты модели.

        Args:
            session: Асинхронная сессия базы данных

        Returns:
            List: Список всех объектов модели
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: Any,
            session: AsyncSession,
            user: Optional[User] = None,
            commit: bool = True
    ) -> ModelType:
        """Создает новый объект модели.

        Args:
            obj_in: Данные для создания объекта
            session: Асинхронная сессия базы данных
            user: Пользователь, создающий объект (опционально)
            commit: Флаг, указывающий нужно ли делать коммит
                    (по умолчанию True)

        Returns:
            Созданный объект модели
        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            obj_in: Any,
            session: AsyncSession,
    ) -> ModelType:
        """Обновляет существующий объект модели.

        Args:
            db_obj: Объект модели для обновления
            obj_in: Данные для обновления объекта
            session: Асинхронная сессия базы данных

        Returns:
            Обновленный объект модели
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        """Удаляет объект модели.

        Args:
            db_obj: Объект модели для удаления
            session: Асинхронная сессия базы данных

        Returns:
            Удаленный объект модели
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj
