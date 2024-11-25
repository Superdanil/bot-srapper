from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserRequest(Base):
    __tablename__ = "users_requests"

    telegram_id: Mapped[int] = mapped_column()
    link: Mapped[str] = mapped_column()
    created_at: Mapped[int] = mapped_column()
