from aiogram.fsm.state import State, StatesGroup


class RandomLinksState(StatesGroup):
    """Машина состояний для получения случайных ссылок."""

    WAITING_FOR_LINK = State()
    FINAL = State()


random_links_state = RandomLinksState()


class LinksPathState(StatesGroup):
    """Машина состояний для получения пути от стартовой статьи к целевой."""

    WAITING_FOR_START_LINK = State()
    WAITING_FOR_TARGET_LINK = State()
    FINAL = State()
