from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Never

from app.core import RepositoryError
from app.core import UserRequest
from app.core import UserRequestReadDTO
from app.repositories.base_repository import BaseRepository


class UserRequestRepository(BaseRepository):
    _model = UserRequest

    async def create(self, value: dict, session: AsyncSession) -> UserRequestReadDTO | Never:
        """Создаёт запись запроса в БД."""
        stmt = insert(self._model).values(value).returning(self._model)
        try:
            result = await session.execute(stmt)
            result = result.scalar_one()
            return self._get_dto(result, UserRequestReadDTO)

        except SQLAlchemyError as e:
            raise RepositoryError(e) from e
