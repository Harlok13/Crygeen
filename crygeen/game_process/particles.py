import random

import pygame as pg
from pygame import Surface, Vector2


class Particle:
    foo = {(0, -1): {'x': (1, -1), 'y': (-1,-1)},
           (0, 1): {'x': (1, -1), 'y': (1,1)},
           (1, 0): {'x': (1,1), 'y': (1, -1)},
           (-1, 0): {'x': (-1, -1), 'y': (1, -1)},
           (.7, -.7): {'x': (1, 1), 'y': (-1,-1)},
           (-.7, -.7): {'x': (-1, -1), 'y': (-1,-1)},
           (-.7, .7): {'x': (-1, -1), 'y': (1, 1)},
           (.7, .7): {'x': (1, 1), 'y': (1, 1)}}

    def __init__(self, position: Vector2, radius: int, color: tuple[int, int, int], direction: Vector2) -> None:
        self.position: Vector2 = position
        self.radius: int = radius
        self.color: tuple = color
        self.direction = Vector2(1, 0)

        self.x_offset: float = random.choice(self.foo.get(tuple(direction.xy))['x']) * random.random()
        self.y_offset: float = random.choice(self.foo.get(tuple(direction.xy))['y']) * random.random() * 4


class ParticlePlayer:

    def __init__(self, surface: Surface) -> None:
        self._particles_list: list[Particle] = []
        self._surface: Surface = surface
        self.object_pos: Vector2 = pg.math.Vector2()
        self.__create_particles_list(100, Vector2(300, 400), 4, (255, 255, 255))

        # self._particles_list: list[Particle] = [Particle(Vector2(600, 400), 4, (255, 0, 0), Vector2(1, 0)) for i in range(50)]
        self._hit: bool = False

    def __create_particles_list(self, amount: int, start_position: Vector2, radius: int, color: tuple) -> None:
        # if self._hit:
        self._particles_list: list[Particle] = [Particle(start_position, radius, color, Vector2(1, 0)) for i in range(amount)]
        for particle in self._particles_list:
            particle.direction = Vector2(1, 0)
            particle.x_offset = random.choice(particle.foo.get(tuple(particle.direction.xy))['x']) * random.random()
            particle.x_offset = random.choice(particle.foo.get(tuple(particle.direction.xy))['x']) * random.random()
        # self._hit: bool = False

    #
    def hit_old(self, amount: int, start_position: Vector2, radius: int, color: tuple[int, int, int]) -> None:
        self._hit: bool = True
        self.__create_particles_list(amount, start_position, radius, color)
        for index, particle in enumerate(self._particles_list):

            particle.position.x += particle.x_offset
            particle.x_offset - 1 if particle.x_offset < 0 else particle.x_offset + 1
            particle.position.y += particle.y_offset

            particle.radius -= 0.3
            pg.draw.circle(self._surface, particle.color, particle.position, particle.radius)
            if particle.radius <= 0:
                self._particles_list.remove(particle)

    def hit(self, amount: int, start_position: Vector2, radius: int, color: tuple[int, int, int]) -> None:
        self._hit: bool = True
        # self.__create_particles_list(amount, start_position, radius, color)
        for index, particle in enumerate(self._particles_list):
            print(particle.x_offset)
            particle.position.x += particle.x_offset
            # particle.x_offset - 1 if particle.x_offset < 0 else particle.x_offset + 1
            particle.position.y += particle.y_offset

            # particle.radius -= 0.3
            pg.draw.circle(self._surface, particle.color, particle.position, particle.radius)
            if particle.radius <= 0:
                self._particles_list.remove(particle)

    def update(self, pos):
        self.hit(200, pos, 4, (255, 0, 0))
