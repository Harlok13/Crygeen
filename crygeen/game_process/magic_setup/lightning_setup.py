import logging
import math
import random
from typing import Optional

import pygame as pg
from pygame import Surface, Vector2

from crygeen.game_process.game_settings import gSettings
from crygeen.utils.support import deprecated


class Lightning:
    def __init__(self, surface: Surface) -> None:
        self.surface: Surface = surface
        self.start_position: Optional[tuple[float, float]] = (0, 0)
        self.x_change: Optional[float] = 0
        self.y_change: Optional[float] = 0
        self.deviation: int = gSettings.LIGHTNING_DEVIATION
        self.length: int = gSettings.LIGHTNING_LENGTH
        self.streaks: int = gSettings.LIGHTNING_STREAKS
        self.color: tuple[int, int, int] = gSettings.LIGHTNING_COLOR
        self.line_width: int = gSettings.LIGHTNING_LINE_WIDTH
        self.range: int = gSettings.LIGHTNING_RANGE

    @deprecated
    def __normalize_vector_old(self):
        """
        Calculate the difference between the coordinates of the points.
        dx = x_end - x_start
        dy = y_end - y_start
        Calculate the length of the vector.
        length = math.sqrt(dx ** 2 + dy ** 2)
        Calculate the normalized direction vector.
        direction_vector = (dx / length, dy / length)

        p.s. The math module already has all these methods, namely Vector2.magnitude()
        and Vector2.length(). But too lazy to write.

        :return: ~(0.8944271909999159 * radius, -0.4472135954999579 * radius)
        """
        mx, my = pg.mouse.get_pos()
        mx -= self.surface.get_width() // 2
        my -= self.surface.get_height() // 2
        start_x, start_y = mx, my

        radius: int = self.range
        if mx > radius:
            mx = radius
        elif mx < -radius:
            mx = -radius
        if my > radius:
            my = radius
        elif my < -radius:
            my = -radius

        vec_length: float = math.sqrt(mx ** 2 + my ** 2)
        normalize_x, normalize_y = (mx / vec_length * radius, my / vec_length * radius)

        self.x_change, self.y_change = normalize_x, normalize_y

    def __normalize_vector(self) -> None:
        """
        Perf old normalize_vector.
        :return: None
        """
        mx, my = pg.mouse.get_pos()
        mx -= self.surface.get_width() // 2
        my -= self.surface.get_height() // 2

        vec = pg.math.Vector2(mx, my)
        vec.scale_to_length(20)
        self.x_change, self.y_change = vec.x, vec.y


    def __render_lightning(self, player_position: tuple[float, float]) -> None:
        self.start_position: tuple[float, float] = player_position
        branch_points: list[tuple[float, float]] = [self.start_position, ]

        self.__normalize_vector()

        for streak in range(self.streaks):
            for length in range(self.length):
                point: tuple[float, float] = branch_points[length]

                new_x_change: float = self.x_change + random.randint(-self.deviation, self.deviation)
                new_y_change: float = self.y_change + random.randint(-self.deviation, self.deviation)

                new_branch_point: tuple[float, float] = (point[0] + new_x_change, point[1] + new_y_change)
                pg.draw.line(self.surface, self.color, point, new_branch_point, self.line_width)
                branch_points.append(new_branch_point)

    def electrify(self) -> None:
        """The effect of lightning hitting an object."""
        pass

    def update(self, player_position: tuple[float, float]) -> None:
        self.__render_lightning(player_position)
