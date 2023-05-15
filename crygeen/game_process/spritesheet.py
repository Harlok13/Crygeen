import json
from pathlib import Path

import pygame as pg
from pygame import Surface

from crygeen.game_process.game_settings import gSettings


class SpriteSheet:
    def __init__(self, filename: Path, metadata: Path):
        self.filename: Path = filename
        self.sprite_sheet: Surface = pg.image.load(self.filename).convert_alpha()
        self.metadata: Path = metadata

        with open(self.metadata) as file:
            self.data: dict = json.load(file)
        file.close()

    def get_sprite(self, x: int, y: int, w: int, h: int) -> Surface:
        sprite: Surface = pg.Surface((w, h))
        sprite.set_colorkey(gSettings.PNG_BG)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, sprite_name: str) -> Surface:
        sprite: dict[str, int] = self.data['frames'][sprite_name]['frame']
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image: Surface = self.get_sprite(x, y, w, h)
        pg.transform.rotate(image, 90.0)
        pg.transform.flip(image, True, False)
        return image



