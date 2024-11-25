from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine: AsyncEngine = create_async_engine(url=url, echo=echo)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        """Закрывает сессию."""
        await self.engine.dispose()

    @asynccontextmanager
    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await self.rollback(session)
                raise e
            finally:
                await session.close()

    @staticmethod
    async def commit(session: AsyncSession):
        """Коммитит изменения в сессии."""
        await session.commit()

    @staticmethod
    async def rollback(session: AsyncSession):
        """Откатывает изменения в сессии."""
        await session.rollback()
