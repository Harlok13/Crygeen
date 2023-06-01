import pygame as pg
from pygame import Rect, Surface

from crygeen.settings import settings


class Cursor:
    def __init__(self) -> None:
        self.img: Surface = pg.image.load(settings.MENU_CURSOR).convert_alpha()
        self.img: Surface = pg.transform.scale(self.img, (30, 50))
        self.rect: Rect = self.img.get_rect()
        self.display_surface: Surface = pg.display.get_surface()

        pg.mouse.set_visible(False)

    def update(self) -> None:
        self.rect.x = pg.mouse.get_pos()[0]
        self.rect.y = pg.mouse.get_pos()[1]
        self.display_surface.blit(self.img, self.rect)
