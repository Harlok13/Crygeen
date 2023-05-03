from crygeen.settings import settings

MIXER_SETTINGS: tuple[int, ...] = (44100, -16, 2, 2048)
BASE_PATH: str = f'{settings.BASE_PATH}/audio'

MAIN_MENU_SOUND: list[str] = [
    f'{BASE_PATH}/main_menu.ogg',
    # f'{BASE_PATH}/main_menu2.ogg',
    # f'{BASE_PATH}/main_menu3.ogg'
]
MAIN_MENU_VOLUME: float = 0.8
MAIN_MENU_LOOPS: int = -1
