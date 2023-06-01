import pygame as pg
from pygame import Vector2


class Enemy(pg.sprite.Sprite):
    def __init__(self, groups, obstacle_sprites, player, particle_player) -> None:
        super().__init__(groups)  # noqa
        self.obstacle_sprites = obstacle_sprites
        self.position: Vector2 = pg.math.Vector2(200, 300)
        self.rect = pg.Rect(self.position.x, self.position.y, 50, 50)

        self.player = player
        self.particle_player = particle_player

    def render(self, surf) -> None:
        if self.player.rect.colliderect(self.rect):
            self.particle_player.update(self.position)
        pg.draw.rect(surf, (255, 255, 255), self.rect)
