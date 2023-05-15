from pathlib import Path

from pydantic import BaseSettings

from crygeen.settings import settings


class GameSettings(BaseSettings):
    GAME_CANVAS_WIDTH: int = 1280
    GAME_CANVAS_HEIGHT: int = 760
    GAME_FPS: int = 60

    PLAYER_SPRITE_SHEET_PATH: Path = settings.BASE_PATH.joinpath('assets', 'graphics', 'player', 'ork.png')
    PLAYER_SPRITE_METADATA_PATH: Path = settings.BASE_PATH.joinpath('assets', 'graphics', 'player', 'ork.json')
    PLAYER_SPEED: int = 200
    PLAYER_SPURT_COEFFICIENT: float = 2
    PLAYER_ANIMATION_SPEED: float = 5
    PLAYER_SPURT_CD: int = 1400
    PLAYER_SPURT_DURATION: int = 300

    PNG_BG: tuple = (0, 0, 0)


gSettings: GameSettings = GameSettings()
