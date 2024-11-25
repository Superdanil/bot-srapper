import time
from datetime import datetime

from app.core import UserRequestCreateDTO, UserRequestReadDTO
from core import DatabaseHelper
from core.settings import settings

from repositories import UserRequestRepository


class DatabaseService:
    """Класс работы с базой данных"""

    def __init__(self, url: str, echo: bool):
        self._repository = UserRequestRepository()
        self._db_helper = DatabaseHelper(url=url, echo=echo)

    async def add_record(self, dto: UserRequestCreateDTO) -> UserRequestReadDTO:
        """Добавляет запись в БД."""
        value = dto.model_dump()
        value["created_at"] = int(time.mktime(datetime.now().timetuple()))

        async with self._db_helper.session_getter() as session:
            new_record = await self._repository.create(value, session)
            await self._db_helper.commit(session)
            return new_record


database_service = DatabaseService(url=settings.DB_URL, echo=settings.ECHO)
