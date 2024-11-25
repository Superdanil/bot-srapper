from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from fsm import RandomLinksState, LinksPathState
from services import wikipedia_service

router = Router(name="wikipedia_router")


@router.message(Command("wikilinks"))
async def get_random_links_start(message: types.Message, state: FSMContext):
    """Обрабатывает команду /wikilinks."""
    msg = await wikipedia_service.get_random_links_start(state=state)
    await message.answer(text=msg)


@router.message(Command("wikipath"))
async def get_page_to_page_path(message: types.Message, state: FSMContext):
    """Обрабатывает команду /wikipath."""
    msg = await wikipedia_service.get_path_start(state=state)
    await message.answer(text=msg)


@router.message(RandomLinksState.WAITING_FOR_LINK)
async def get_random_links_done(message: types.Message, state: FSMContext):
    """Принимает от пользователя статью для парсинга случайных ссылок."""
    msg = await wikipedia_service.get_random_links_done(message=message, state=state)
    await message.reply(text=msg, disable_web_page_preview=True)


@router.message(LinksPathState.WAITING_FOR_START_LINK)
async def post_start_link(message: types.Message, state: FSMContext):
    """Принимает от пользователя стартовую статью для построения пути."""
    msg = await wikipedia_service.get_path_continue(message=message, state=state)
    await message.answer(text=msg)


@router.message(LinksPathState.WAITING_FOR_TARGET_LINK)
async def post_target_link(message: types.Message, state: FSMContext):
    """Принимает от пользователя целевую статью для построения пути."""
    msg = await wikipedia_service.get_path_done(message=message, state=state)
    await message.answer(text=msg, disable_web_page_preview=True)
