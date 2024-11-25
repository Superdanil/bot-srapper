import asyncio
import random
from collections import deque
from urllib.parse import unquote

import aiohttp
from bs4 import BeautifulSoup

from core.log_handler import logger
from core.settings import settings


class Scraper:
    excluded_conditions = {"#", "?", ":", ".jpg", ".png", "заглавная_страница", "Заглавная_страница"}

    def __init__(self, max_depth: int):
        self.max_depth = max_depth
        self.visited = set()

    @classmethod
    async def get_random_links(cls, wiki_page: str) -> set[str]:
        """Возвращает RANDOM_LINKS_COUNT ссылок из статьи Википедии."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(wiki_page) as response:
                    content = await response.text()
            except aiohttp.ClientError as e:
                logger.error(e)

            soup = BeautifulSoup(content, "html.parser")
            links = set()

            for a_tag in soup.find_all("a", href=True):
                href = unquote(a_tag["href"])
                if href.startswith("/wiki/") and not any(item in href for item in cls.excluded_conditions):
                    links.add(f"https://ru.wikipedia.org{href}")
                if href.startswith('http://') or href.startswith('https://') and not "wikipedia.org" in href:
                    links.add(href)

            random_links = random.sample(tuple(links), settings.RANDOM_LINKS_COUNT)
            return random_links

    async def get_path(self, start_link: str, target_link: str) -> list[str] | None:
        """Широкий поиск по связям (BFS) для нахождения пути между двумя статьями."""
        async with aiohttp.ClientSession() as session:
            queue = deque([(start_link, [start_link])])  # Очередь для хранения текущей ссылки и пути к ней
            tasks = []
            while queue:
                for link, path in queue:
                    if link in self.visited:
                        continue

                    self.visited.add(link)

                    if len(path) > self.max_depth + 1:
                        self.visited.clear()
                        return None  # Путь не найден

                    if link == target_link:
                        self.visited.clear()
                        return path

                    tasks.append(self._get_wiki_links(session, link, path))
                links = await asyncio.gather(*tasks)
                tasks.clear()
                for links, path in links:
                    for link in links:
                        if link not in self.visited:
                            queue.append((link, path + [link]))

        self.visited.clear()
        return None  # Путь не найден

    async def _get_wiki_links(
            self,
            session: aiohttp.ClientSession,
            wiki_page: str,
            path: list[str],
    ) -> tuple[set[str], list[str]]:
        """Возвращает все ссылки из указанной статьи Википедии."""
        try:
            async with session.get(wiki_page) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")
        except aiohttp.ClientError as e:
            logger.error(e)

        links = set()

        for a in soup.find_all("a", href=True):
            href = unquote(a["href"])
            # Проверяем, что ссылка ведет на статью Википедии
            if href.startswith("/wiki/") and not any(item in href for item in self.excluded_conditions):
                links.add(f"https://ru.wikipedia.org{href}")

        return links, path


scraper = Scraper(settings.MAX_DEPTH)
