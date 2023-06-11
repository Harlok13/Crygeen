import random
from typing import Any

import pygame as pg
from pygame import Surface, Vector2

from crygeen.game_process.game_settings import gSettings, ParticleDirection, ParticleRadius
from crygeen.utils.support import deprecated


class ParticleBlood:
    """One piece of blood"""

    def __init__(
            self,
            pos_x: int,
            pos_y: int,
            radius: ParticleRadius,
            direction_x: ParticleDirection,
            direction_y: ParticleDirection,
            duration: int,
            start_time: int
    ) -> None:

        self.pos_x: int = pos_x
        self.pos_y: int = pos_y
        self.pos_vec: Vector2 = pg.Vector2(self.pos_x, self.pos_y)

        self.radius: int = radius.start_radius  # TODO: ref title cuz its not a radius
        self.dest_radius: int = random.randint(radius.start_radius, radius.dest_radius)

        self.direction_x: int = random.randint(*direction_x)
        self.direction_y: int = random.randint(*direction_y)
        self.dir_vec: Vector2 = pg.Vector2(self.direction_x, self.direction_y)

        # normalize vector to circle
        if self.dir_vec.length() == 0:
            self.dir_vec.x = 1
        self.dir_vec.scale_to_length(min(self.dir_vec.length(), direction_x.positive))  # TODO: or make ellipse? ValueError: Cannot scale a vector with zero length

        self.dest_vec: Vector2 = pg.Vector2(self.pos_vec + self.dir_vec)

        self.duration: int = duration
        self.start_time: int = start_time

        self.color: tuple[int, int, int] = random.choice(gSettings.BLOOD_COLORS)

        self.image = pg.Surface((radius.dest_radius * 2, radius.dest_radius * 2)).convert_alpha()
        self.image.fill('white')
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect(center=self.pos_vec)

        self.lifetime: int = gSettings.BLOOD_PARTICLE_LIFETIME

        self.offset_rect = self.rect


class BloodParticlePlayer:
    def __init__(self, canvas) -> None:
        self.particles: list[ParticleBlood] = []
        self.particles_amount: int = gSettings.BLOOD_PARTICLE_AMOUNT

        self.canvas: Surface = canvas

        self.screen_size: tuple[float, float] = pg.display.get_window_size()

    @staticmethod
    def __lerp(a, b, dt) -> float:  # noqa
        return a + (b - a) * dt

    def emit(self, player) -> None:
        self.__delete_particles(player)

        if self.particles:

            for particle in self.particles:

                delta: int = pg.time.get_ticks() - particle.start_time

                if delta < particle.duration:

                    particle.pos_vec = self.__lerp(
                        particle.pos_vec, particle.dest_vec, delta / particle.duration
                    )

                    particle.radius = self.__lerp(
                        particle.radius, particle.dest_radius, delta / particle.duration
                    )

                particle.rect = particle.image.get_rect(center=particle.pos_vec)

                pg.draw.ellipse(
                    self.canvas, particle.color,
                    pg.Rect(particle.rect.centerx - player.rect.centerx, particle.rect.centery - player.rect.centery,
                            particle.radius, particle.radius // 2),
                )

            # change particle lifetime
            for particle in self.particles:
                particle.lifetime -= random.random() * gSettings.PARTICLE_LIFETIME_COEFFICIENT

    def add_particles(self, entity: Any) -> None:

        particle_circle: ParticleBlood = ParticleBlood(
            pos_x=entity.rect.centerx + self.screen_size[0] / 2,  # TODO: must be hitbox
            pos_y=entity.rect.centery + self.screen_size[1] / 2,
            radius=gSettings.BLOOD_PARTICLE_RADIUS,
            direction_x=gSettings.BLOOD_PARTICLE_DIRECTION_X,
            direction_y=gSettings.BLOOD_PARTICLE_DIRECTION_Y,
            duration=gSettings.BLOOD_PARTICLE_DURATION,
            start_time=pg.time.get_ticks()
        )
        # self.particles: list[ParticleBlood] = [
        #     particle_circle for _ in range(self.particles_amount)
        # ]
        self.particles.append(particle_circle)

    def __delete_particles(self, player) -> None:
        particle_copy: list[ParticleBlood] = [particle for particle in self.particles if particle.lifetime > 0]
        self.particles: list[ParticleBlood] = particle_copy

    @deprecated
    def update(self, player,  *args, **kwargs) -> None:
        self.add_particles()
        self.emit(player)

