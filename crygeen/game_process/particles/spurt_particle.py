import random

import pygame as pg
from pygame import Surface, Vector2

from crygeen.game_process.game_settings import gSettings, ParticleDirection, ParticleRadius
from crygeen.game_process.player_setup.player import Player


class ParticleSpurt:
    def __init__(
            self,
            # pos_x: int,
            # pos_y: int,
            radius: ParticleRadius,
            # direction_x: ParticleDirection,
            # direction_y: ParticleDirection,
            duration: int,
            start_time: int,
            player: Player
    ) -> None:
        self.screen_size = pg.display.get_window_size()

        self.half_width: int = self.screen_size[0] // 2
        self.half_height: int = self.screen_size[1] // 2
        self.pos_x: int = player.rect.centerx + self.half_width
        self.pos_y: int = player.rect.centery + self.half_height
        self.pos_vec: Vector2 = pg.Vector2(self.pos_x, self.pos_y)

        self.player: Player = player

        self.radius: int = 15  # TODO: ref title cuz its not a radius
        self.dest_radius: int = -5

        self.direction_x: int = -self.player.keyboard_input.direction.x * random.randint(5, 150) + random.randint(-200, 200) # TODO: normalize vector
        self.direction_y: int = -self.player.keyboard_input.direction.y * random.randint(5, 150) + random.randint(-200, 200)
        self.dir_vec: Vector2 = pg.Vector2(self.direction_x, self.direction_y)

        self.dest_vec: Vector2 = pg.Vector2(self.pos_vec + self.dir_vec)

        self.duration: int = 3000
        self.start_time: int = start_time

        self.color: tuple[int, int, int] = random.choice(((89, 2, 2), (102, 2, 2), (115, 3, 3), (66, 3, 3), (35, 2, 2), (10, 1, 1)))

        self.image = pg.Surface((radius.dest_radius * 2, radius.dest_radius * 2)).convert_alpha()
        self.image.fill('white')
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect(center=self.pos_vec)

        self.lifetime: int = gSettings.BLOOD_PARTICLE_LIFETIME

        self.offset_rect = self.rect


class SpurtParticlePlayer(pg.sprite.Sprite):
    def __init__(self, group) -> None:
        super().__init__(group)
        self.particles: list[ParticleSpurt] = []
        self.particles_amount: int = gSettings.BLOOD_PARTICLE_AMOUNT

        self.group = group

    @staticmethod
    def __lerp(a, b, dt) -> float:  # noqa
        return a + (b - a) * dt

    def emit(self, canvas: Surface, player) -> None:
        self.__delete_particles()

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

                particle.rect = particle.image.get_rect(center=(particle.pos_x, particle.pos_y))

                # pg.draw.circle(
                #     canvas, particle.color, (particle.rect.centerx - player.rect.centerx, particle.rect.centery - player.rect.centery), int(particle.radius)
                # )

                pg.draw.ellipse(
                    canvas, particle.color,
                    pg.Rect(particle.rect.centerx - player.rect.centerx, particle.rect.centery - player.rect.centery,
                            particle.radius, particle.radius // 2),
                )

            # change particle lifetime
            for particle in self.particles:
                particle.lifetime -= random.random() * gSettings.PARTICLE_LIFETIME_COEFFICIENT

    def add_particles(self, player) -> None:  # TODO: use as API

        particle_circle: ParticleSpurt = ParticleSpurt(
            # pos_x=pg.mouse.get_pos()[0],
            # pos_y=pg.mouse.get_pos()[1],
            radius=gSettings.BLOOD_PARTICLE_RADIUS,
            # direction_x=gSettings.BLOOD_PARTICLE_DIRECTION_X,
            # direction_y=gSettings.BLOOD_PARTICLE_DIRECTION_Y,
            duration=gSettings.BLOOD_PARTICLE_DURATION,
            start_time=pg.time.get_ticks(),
            player=player
        )
        # self.particles: list[ParticleSpurt] = [
        #     particle_circle for _ in range(self.particles_amount)
        # ]
        self.particles.append(particle_circle)

    def __delete_particles(self) -> None:
        particle_copy: list[ParticleSpurt] = [particle for particle in self.particles if particle.lifetime > 0]
        self.particles: list[ParticleSpurt] = particle_copy

    def update(self, canvas: Surface, player,  *args, **kwargs) -> None:
        self.add_particles(player)
        self.emit(canvas, player)
