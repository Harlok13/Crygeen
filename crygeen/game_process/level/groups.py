import pygame as pg
from pygame import Surface, Vector2, Rect


class Groups:
    def __init__(self, canvas: Surface) -> None:

        self.visible_sprites: CameraGroup = CameraGroup(canvas)
        self.particles_group: ParticleGroup = ParticleGroup(canvas)
        self.obstacle_sprites = pg.sprite.Group()
        self.light_sprites = pg.sprite.Group()
        self.grass_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()


class CameraGroup(pg.sprite.Group):  # todo add mixin?
    def __init__(self, canvas: Surface) -> None:
        super().__init__()
        self.canvas: Surface = canvas
        self.screen: Surface = pg.display.get_surface()
        self.offset: Vector2 = pg.math.Vector2()

    def custom_render(self, player) -> None:
        self.offset.x = player.rect.centerx - self.screen.get_width() / 2
        self.offset.y = player.rect.centery - self.screen.get_height() / 2

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):  # noqa
            offset_rect: Rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.canvas.blit(sprite.image, offset_rect)

            self.screen.blit(self.canvas, (0, 0))


class ParticleGroup(pg.sprite.Group):
    def __init__(self, canvas: Surface) -> None:
        super().__init__()
        self.canvas: Surface = canvas
        self.screen: Surface = pg.display.get_surface()
        self.offset: Vector2 = pg.Vector2()

    def custom_render(self, player) -> None:
        self.offset.x = player.rect.centerx - self.screen.get_width()
        self.offset.y = player.rect.centery - self.screen.get_height()

        for group in self.sprites():
            for particle in group.particles:

                offset_rect: Rect = particle.rect.copy()
                offset_rect.center -= self.offset
                particle.offset_rect = offset_rect

                self.screen.blit(self.canvas, (0, 0))
