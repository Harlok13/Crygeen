import operator
import random

import pygame as pg
from pygame import Surface


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
