from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserRequestCreateDTO(BaseModel):
    telegram_id: int
    link: str

    model_config = ConfigDict(from_attributes=True)


class UserRequestReadDTO(UserRequestCreateDTO):
    id: UUID
    created_at: datetime
