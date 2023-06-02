import os
from pathlib import Path

from pydantic import BaseSettings

from crygeen.settings import settings


class GameSettings(BaseSettings):
    GAME_CANVAS_WIDTH: int = 1280
    GAME_CANVAS_HEIGHT: int = 760
    GAME_FPS: int = 60
    PNG_BG: tuple = (0, 0, 0)

    PLAYER_SPRITE_SHEET_PATH: Path = settings.BASE_PATH.joinpath('assets', 'graphics', 'player', 'ork.png')
    PLAYER_SPRITE_METADATA_PATH: Path = settings.BASE_PATH.joinpath('assets', 'graphics', 'player', 'ork.json')
    PLAYER_SPEED: int = 200
    PLAYER_SPURT_COEFFICIENT: float = 2
    PLAYER_ANIMATION_SPEED: float = 5
    PLAYER_SPURT_CD: int = 1400
    PLAYER_SPURT_DURATION: int = 300
    PLAYER_ATTACK_CD: int = 700

    # GRASS_PATH: Path = settings.BASE_PATH.joinpath('assets', 'graphics', 'grass')
    GRASS_PATH: str = '/Users/harlok/PycharmProjects/Crygeen/crygeen/assets/graphics/grass'  # TODO: ref hardcode
    GRASS_TILE_SIZE: int = 10
    GRASS_SHADE_AMOUNT: int = 100
    GRASS_STIFFNESS: int = 360
    GRASS_MAX_UNIQUE: int = 10
    GRASS_PLACE_RANGE: list[int, int] = [0, 1]
    GRASS_PADDING: int = 13
    GRASS_ROTATION_SPEED: float = 100
    # shadows
    GRASS_SHADOW_STRENGTH: int = 40
    GRASS_SHADOW_RADIUS: int = 2
    GRASS_SHADOW_COLOR: tuple[int, int, int] = (0, 0, 1)
    GRASS_SHADOW_SHIFT: tuple[int, int] = (0, 0)

    LIGHTNING_DEVIATION: int = 10
    LIGHTNING_LENGTH: int = 10
    LIGHTNING_STREAKS: int = 2
    LIGHTNING_COLOR: tuple[int, int, int] = (0, 255, 255)
    LIGHTNING_LINE_WIDTH: int = 2
    LIGHTNING_RANGE: int = 20

    NIGHT_COLOR: tuple[int, int, int] = (255, 255, 255)
    DAY_DURATION: int = 100000
    NIGHT_DURATION: int = 30000
    DAWN_START: int = NIGHT_DURATION // 2


gSettings: GameSettings = GameSettings()
