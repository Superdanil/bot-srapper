import http
from typing import Iterable
from urllib.parse import unquote

import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core import UserRequestCreateDTO
from core.log_handler import logger
from fsm import RandomLinksState, LinksPathState
from services import database_service, scraper


class WikipediaService:

    def __init__(self):
        self.start_link: str | None = None
        self.target_link: str | None = None

    @staticmethod
    async def get_random_links_start(state: FSMContext) -> str:
        """Возвращает текст с предложением пользователю ввести ссылку на статью."""
        await state.set_state(RandomLinksState.WAITING_FOR_LINK)

        return "Отправьте ссылку на статью Wikipedia"

    async def get_random_links_done(self, message: Message, state: FSMContext) -> str:
        """Добавляет запрос пользователя в БД, возвращает отформатированную строку со случайными ссылками из статьи."""
        await state.set_state(RandomLinksState.FINAL)
        link = unquote(message.text)

        dto = UserRequestCreateDTO(telegram_id=message.from_user.id, link=link)
        if not await database_service.add_record(dto):
            return "Сервис временно недоступен"

        if not await self._is_ru_wikipedia_link(link):
            return "Некорректная ссылка"

        links = await scraper.get_random_links(link)

        return self._serialize_linklist(links)

    @staticmethod
    async def _is_ru_wikipedia_link(wiki_page: str) -> bool:
        """Возвращает True, если ссылка ведёт на статью русскоязычной Википедии, иначе - False."""
        if not wiki_page.startswith("https://ru.wikipedia.org/wiki/") and any(
                item in wiki_page for item in scraper.excluded_conditions):
            return False

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(wiki_page) as response:
                    return response.status == http.HTTPStatus.OK
            except aiohttp.ClientError as e:
                logger.error(e)

    @staticmethod
    def _serialize_linklist(links: Iterable[str]) -> str:
        """Форматирует список ссылок."""
        return "\n\n".join(f"{link}" for link in links)

    @staticmethod
    async def get_path_start(state: FSMContext) -> str:
        """Возвращает текст с предложением пользователю ввести ссылку на первую статью."""
        await state.set_state(LinksPathState.WAITING_FOR_START_LINK)

        return "Отправьте ссылку на первую статью Wikipedia. Напоминаю, поиск может занять несколько минут."

    async def get_path_continue(self, message: Message, state: FSMContext) -> str:
        """Принимает и проверяет ссылку на стартовую статью Википедии.
        Возвращает текст с предложением пользователю ввести ссылку на вторую статью."""
        await state.set_state(LinksPathState.WAITING_FOR_TARGET_LINK)

        self.start_link = unquote(message.text)

        dto = UserRequestCreateDTO(telegram_id=message.from_user.id, link=self.start_link)
        if not await database_service.add_record(dto):
            return "Сервис временно недоступен"

        if not await self._is_ru_wikipedia_link(message.text):
            return "Некорректная ссылка. Попробуйте еще раз: /wikipath"

        return "Отлично! Отправьте ссылку на вторую статью"

    async def get_path_done(self, message: Message, state: FSMContext) -> str:
        """Принимает и проверяет ссылку на целевую статью Википедии.
        Возвращает строку со списком ссылок от первой статьи до второй."""
        await state.set_state(LinksPathState.FINAL)

        self.target_link = unquote(message.text)

        dto = UserRequestCreateDTO(telegram_id=message.from_user.id, link=self.target_link)
        if not await database_service.add_record(dto):
            return "Сервис временно недоступен"

        if not await self._is_ru_wikipedia_link(self.target_link):
            return "Некорректная ссылка. Попробуйте еще раз: /wikipath"

        path = await scraper.get_path(self.start_link, self.target_link)

        if not path:
            return f"Пути от {self.start_link} до {self.target_link} не найдено"

        return self._serialize_linklist(path)


wikipedia_service = WikipediaService()
