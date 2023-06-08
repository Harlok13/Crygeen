"""
This is experimental module
"""
import math
import operator
import random

import pygame as pg
from pygame import Surface

from crygeen.utils.light_engine import Light, pixel_shader, global_light


class LightParticle:
    def __init__(self) -> None:
        # general setup
        self.screen_size: tuple[int, int] = pg.display.get_window_size()
        self.speed: float = random.random()
        self.size: int = int(random.random() * 10)
        self.intensity: float = random.random()
        self.light: Light = Light(25, pixel_shader(self.size, (255, 255, 255), self.intensity, point=False))

        # get start point
        self.x: int = random.randint(0, self.screen_size[0])
        self.y: int = random.randint(0, self.screen_size[1])

        # get end point
        self.target_x: int = random.randint(0, self.screen_size[0])
        self.target_y: int = random.randint(0, self.screen_size[1])

        self.change_size: float = 0

    def move(self) -> None:

        distance_x: int = self.target_x - self.x
        distance_y: int = self.target_y - self.y

        distance_total: float = math.sqrt(distance_x ** 2 + distance_y ** 2)

        dx: float = distance_x / distance_total
        dy: float = distance_y / distance_total

        self.speed: float = random.uniform(0.5, 2)

        x_offset: float = random.random() * random.choice((2, -2))
        y_offset: float = random.random() * random.choice((2, -2))

        if distance_total > self.speed:
            self.x += dx * self.speed + x_offset
            self.y += dy * self.speed + y_offset
            # if self.change_size < 10:
            #     self.change_size += 0.1
            #     self.size = int(self.change_size)
            # if distance_total < 300:
            #     self.change_size += 0.1
            #     self.size -= int(self.change_size)
            #     if self.size < 0:
            #         self.size = 1
        else:
            self.x = random.randint(0, self.screen_size[0])
            self.y = random.randint(0, self.screen_size[1])
            self.size: int = int(random.random() * 10)
        # self.light: Light = Light(25, pixel_shader(self.size, (255, 255, 255), self.intensity, point=False))

    def draw(self, screen: Surface) -> None:
        self.light.main([], screen, self.x, self.y)


class LightParticlePlayer:
    def __init__(self):
        self.particles = [LightParticle() for i in range(100)]

    @staticmethod
    def __set_lights_display(screen: Surface) -> None:
        # screen.fill((255, 255, 255))

        lights_display: Surface = pg.Surface(screen.get_size())
        lights_display.blit(global_light(screen.get_size(), 150), (0, 0))

        screen.blit(lights_display, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

    def render(self, screen: Surface) -> None:
        self.__set_lights_display(screen)

        for particle in self.particles:
            particle.move()
            particle.draw(screen)


class Particle:
    def __init__(self, pos: list[float, float], color, glow_color, radius: float, glow_radius, surf) -> None:
        self.pos = pos
        self.color = color
        self.glow_color = glow_color
        self.radius: float = radius
        self.glow_radius: float = radius * glow_radius  # must be > 2 validate
        self.surf = {'circle': self.circle_surf}.get(surf)()  # validate

    def circle_surf(self) -> Surface:
        surf: Surface = pg.Surface((self.glow_radius * 2, self.glow_radius * 2))
        pg.draw.circle(surf, self.glow_color, (self.glow_radius, self.glow_radius), self.glow_radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def __glow_radius_pulsing(self):
        pass

    def __glow_opacity_pulsing(self):
        pass


class ParticlePlayer:
    def __init__(self):

        self.particles = self.__create_menu_particles(20)

    def __create_menu_particles(self, particles_amount) -> list[Particle]:
        particles = []
        for particle in range(particles_amount):
            part = Particle(
                pos=[random.randint(50, 1000), random.randint(50, 700)],
                color=(255, 255, 255),
                glow_color=(0, 80, 0),
                radius=3,
                glow_radius=3,
                surf='circle'
            )
            particles.append(part)
        return particles

    def display_particle_menu_effect(self, surface: Surface, particles_amount: int = 20) -> None:
        # particles: list[Particle] = self.__create_menu_particles(particles_amount)
        op = random.choice((operator.isub, operator.iadd))
        for particle in self.particles:
            # op1 =
            particle.pos[0] += random.randint(-5, 5)
            particle.pos[1] += random.randint(-5, 5)

            pg.draw.circle(surface, particle.color, particle.pos, particle.radius)
            surface.blit(particle.surf,
                         (int(particle.pos[0] - particle.radius * 3), int(particle.pos[1] - particle.radius * 3)),
                         special_flags=pg.BLEND_RGBA_ADD)
