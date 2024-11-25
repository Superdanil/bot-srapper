from app.core import Base


class BaseRepository:
    @staticmethod
    def _get_dto(row: Base, dto_model):
        """Возвращает Pydantic-schema из SQLA-model."""
        return dto_model.model_validate(row)
