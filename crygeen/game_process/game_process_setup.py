import pygame as pg
from pygame import Surface

from crygeen.game_process.game_settings import gSettings
from crygeen.game_process.level import Level
from crygeen.game_process.spritesheet import SpriteSheet
from pygame import QUIT, KEYDOWN, KEYUP, Surface, MOUSEBUTTONDOWN, MOUSEWHEEL


class GameProcessSetup:
    def __init__(self):
        self.game_canvas: Surface = pg.Surface(
            (gSettings.GAME_CANVAS_WIDTH, gSettings.GAME_CANVAS_HEIGHT)
        )
        self.fps: int = gSettings.GAME_FPS

        self.sprite_sheet: SpriteSheet = SpriteSheet(
            gSettings.PLAYER_SPRITE_SHEET_PATH, gSettings.PLAYER_SPRITE_METADATA_PATH
        )
        pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEWHEEL])

        self.level: Level = Level(self, self.sprite_sheet)
