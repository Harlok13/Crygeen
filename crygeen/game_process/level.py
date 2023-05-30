import pygame as pg
from pygame import Surface

from crygeen.game_process.enemy import Enemy
from crygeen.game_process.grass_setup.grass_api import Grass
from crygeen.game_process.magic_setup.lightning_setup import Lightning
from crygeen.game_process.player_setup.player import Player
from crygeen.game_process.spritesheet import SpriteSheet
from crygeen.game_process.particles import ParticlePlayer


class Level:
    def __init__(self, game, sprite_sheet):  # type: ('Game', SpriteSheet) -> None
        # general setup _____________________________________________________________________________
        self.game_canvas: Surface = game.game_canvas
        self.game_paused: bool = False

        self.sprite_sheet: SpriteSheet = sprite_sheet

        # sprite group setup ________________________________________________________________________
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()

        self.grass: Grass = Grass()

        # player setup ______________________________________________________________________________
        self.player: Player = Player([self.visible_sprites], self.obstacle_sprites, self.sprite_sheet)

        # magic
        self.lightning: Lightning = Lightning(self.game_canvas)

        self.particle_player: ParticlePlayer = ParticlePlayer(self.game_canvas)

        self.enemy: Enemy = Enemy([self.visible_sprites], self.obstacle_sprites, self.player, self.particle_player)

    def run(self, dt: float) -> None:
        self.game_canvas.fill((27, 66, 52))
        self.player.update(dt)
        self.grass.render(dt, self.game_canvas, self.player)
        self.game_canvas.blit(self.player.image, self.player.rect)
        self.particle_player.update(pg.math.Vector2(600, 400))

        if self.player.keyboard_input.lightning:
            self.lightning.update(self.player.rect.center)

        self.enemy.render(self.game_canvas)



class YSortCameraGroup(pg.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
