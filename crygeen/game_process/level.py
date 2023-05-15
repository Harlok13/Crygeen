import pygame as pg
from pygame import Surface

from crygeen.game_process.player import Player


class Level:
    def __init__(self, game, sprite_sheet):  # type: ('Game', 'SpriteSheet') -> None
        # general setup _____________________________________________________________________________
        self.game_canvas: Surface = game.game_canvas
        self.game_paused: bool = False

        self.sprite_sheet = sprite_sheet

        # sprite group setup ________________________________________________________________________
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()

        self.player = Player([self.visible_sprites], self.obstacle_sprites, self.sprite_sheet)

    def run(self, dt):
        self.player.update(dt)
        self.game_canvas.fill('white')
        self.game_canvas.blit(self.player.image, self.player.rect)


class YSortCameraGroup(pg.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
