import pygame as pg
from pygame import Rect, Surface, Vector2

from crygeen.game_process.player_setup.player_animation import PlayerAnimation
from crygeen.game_process.player_setup.player_keyboard_input import PlayerKeyboardInput
from crygeen.game_process.player_setup.player_stats import PlayerStats
from crygeen.game_process.spritesheet import SpriteSheet
from crygeen.settings import settings


class Player(pg.sprite.Sprite):

    def __init__(self, groups, obstacle_sprites, sprite_sheet: SpriteSheet) -> None:
        super().__init__(groups)  # type: ignore
        # general setup _____________________________________________________________________________
        self.sprite_sheet: SpriteSheet = sprite_sheet
        self.image: Surface = self.sprite_sheet.get_sprite(76, 110, 76, 55)

        self.rect: Rect = self.image.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2))  # todo ref
        self.hitbox: Rect = self.rect

        self.obstacle_sprites = obstacle_sprites

        self.keyboard_input: PlayerKeyboardInput = PlayerKeyboardInput(self)
        self.animation: PlayerAnimation = PlayerAnimation(self)
        self.stats: PlayerStats = PlayerStats()

    def update(self, dt: float) -> None:
        self.keyboard_input.update(dt)
        self.animation.render(dt, self.keyboard_input.status)
