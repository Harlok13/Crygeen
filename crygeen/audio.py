from pathlib import Path

MIXER_SETTINGS: tuple[int, ...] = (44100, -16, 2, 2048)
BASE_AUDIO_PATH: Path = Path(__file__).parent.joinpath('assets', 'audio').resolve()

MAIN_MENU_SOUND: list[str | Path] = [
    BASE_AUDIO_PATH.joinpath('main_menu.mp3'),
    BASE_AUDIO_PATH.joinpath('main_menu2.mp3'),
    # f'{BASE_PATH}/main_menu3.ogg'
]
MAIN_MENU_VOLUME: float = 0.8
MAIN_MENU_LOOPS: int = -1

SOUND_CLICK: Path = BASE_AUDIO_PATH.joinpath('click.ogg')
