import random

import pygame as pg
from pygame import Surface, Vector2

from crygeen.game_process.game_settings import gSettings, ParticleDirection, ParticleRadius


class ParticleBlood(pg.sprite.Sprite):
    """One piece of blood"""

    def __init__(
            self,
            group,
            pos_x: int,
            pos_y: int,
            radius: ParticleRadius,
            direction_x: ParticleDirection,
            direction_y: ParticleDirection,
            duration: int,
            start_time: int
    ) -> None:

        super().__init__(group)
        self.pos_x: int = pos_x
        self.pos_y: int = pos_y
        self.pos_vec: Vector2 = pg.Vector2(self.pos_x, self.pos_y)

        self.radius: int = radius.start_radius
        self.dest_radius: int = random.randint(radius.start_radius, radius.dest_radius)

        self.direction_x: int = random.randint(*direction_x)
        self.direction_y: int = random.randint(*direction_y)
        self.dir_vec: Vector2 = pg.Vector2(self.direction_x, self.direction_y)

        self.dest_vec: Vector2 = pg.Vector2(self.pos_vec + self.dir_vec)

        self.duration: int = duration
        self.start_time: int = start_time

        self.color: tuple[int, int, int] = random.choice(gSettings.BLOOD_COLORS)

        self.image = pg.Surface((radius.dest_radius * 2, radius.dest_radius * 2)).convert_alpha()
        self.image.fill('white')
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect(center=self.pos_vec)

        self.lifetime: int = gSettings.BLOOD_PARTICLE_LIFETIME


class ParticlePlayer:
    def __init__(self, group) -> None:
        self.particles: list[ParticleBlood] = []
        self.particles_amount: int = gSettings.BLOOD_PARTICLE_AMOUNT

        self.group = group

    @staticmethod
    def __lerp(a, b, dt) -> float:  # noqa
        return a + (b - a) * dt

    def emit(self) -> None:
        self.delete_particles()

        if self.particles:

            for particle in self.particles:

                delta: int = pg.time.get_ticks() - particle.start_time

                if delta < particle.duration:
                    particle.pos_x = self.__lerp(
                        particle.pos_vec.x, particle.dest_vec.x, delta / particle.duration
                    )

                    particle.pos_y = self.__lerp(
                        particle.pos_vec.y, particle.dest_vec.y, delta / particle.duration
                    )

                    particle.radius = self.__lerp(
                        particle.radius, particle.dest_radius, delta / particle.duration
                    )

                pg.draw.circle(
                    particle.image, particle.color, (particle.pos_x, particle.pos_y), int(particle.radius)
                )
                particle.rect = particle.image.get_rect(center=(particle.pos_x, particle.pos_y))

            # change particle lifetime
            for particle in self.particles:
                particle.lifetime -= random.random() * gSettings.PARTICLE_LIFETIME_COEFFICIENT

    def add_particles(self) -> None:

        particle_circle: ParticleBlood = ParticleBlood(
            group=self.group,
            pos_x=pg.mouse.get_pos()[0],
            pos_y=pg.mouse.get_pos()[1],
            radius=gSettings.BLOOD_PARTICLE_RADIUS,
            direction_x=gSettings.BLOOD_PARTICLE_DIRECTION_X,
            direction_y=gSettings.BLOOD_PARTICLE_DIRECTION_Y,
            duration=gSettings.BLOOD_PARTICLE_DURATION,
            start_time=pg.time.get_ticks()
        )
        self.particles: list[ParticleBlood] = [
            particle_circle for _ in range(self.particles_amount)
        ]
        self.particles.append(particle_circle)

    def delete_particles(self) -> None:
        particle_copy: list[ParticleBlood] = [particle for particle in self.particles if particle.lifetime > 0]
        self.particles: list[ParticleBlood] = particle_copy

    def update(self, *args, **kwargs) -> None:
        print(kwargs)
        if kwargs['collide']:
            self.add_particles()
            self.emit()

