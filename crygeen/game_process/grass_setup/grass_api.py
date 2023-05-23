import random
import math
from typing import Callable

from pygame import Surface

from crygeen.game_process.game_settings import gSettings
from crygeen.game_process.grass_setup.grass_manager import GrassManager


class Grass:
    def __init__(self) -> None:
        self.__grass_manager: GrassManager = GrassManager(gSettings.GRASS_PATH)
        self.__grass_manager.enable_ground_shadows()
        self.__rotation_speed: float = gSettings.GRASS_ROTATION_SPEED

        self._t: float = 0

    def place_grass(self) -> None:
        for y in range(25):
            y += 5
            for x in range(100):
                x += 5
                v = random.random()
                if v > 0.1:
                    self.__grass_manager.place_tile((x, y), int(v * 12), [0, 1, 2, 3, 4])

    def render(self, dt: float, screen: Surface, player) -> None:
        self.__grass_manager.apply_force(player.rect.center, 15, 25)

        rot_function: Callable = lambda x, y: int(math.sin(self._t / 60 + x / 100) * 15)  # TODO: reloc to settings

        self.__grass_manager.update_render(screen, dt, rot_function=rot_function)
        self._t += dt * self.__rotation_speed
        self.place_grass()
