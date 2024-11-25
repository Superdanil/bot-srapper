from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from core.settings import settings

router = Router(name="support_router")


@router.message(CommandStart())
async def start_message(message: types.Message):
    """Обрабатывает команду /start."""
    await message.answer(
        text="Привет! Я wikipedia-бот, и вот что я умею:\n"
             f"Я могу прислать {settings.RANDOM_LINKS_COUNT} случайных ссылок со статьи на сайте "
             f"https://ru.wikipedia.org по команде /wikilinks, или я могу построить тебе путь по ссылкам "
             f"от одной статьи до другой по команде /wikipath",
        disable_web_page_preview=True,
    )


@router.message(Command("help"))
async def help_message(message: types.Message):
    """Обрабатывает команду /help."""
    await message.answer(
        text=f"/wikilinks - получить {settings.RANDOM_LINKS_COUNT} случайных ссылок со статьи на сайте "
             f"https://ru.wikipedia.org\n"
             f"/wikipath - построить путь по ссылкам от одной статьи до другой. Максимальная длина пути не может"
             f"превышать {settings.MAX_DEPTH}",
        disable_web_page_preview=True,
    )
