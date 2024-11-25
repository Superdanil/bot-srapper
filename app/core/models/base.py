import uuid
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    id: Mapped[UUID] = mapped_column(unique=True, primary_key=True, default=uuid.uuid4)
