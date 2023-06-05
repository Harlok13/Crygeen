import os
from pathlib import Path

import pygame as pg
from pygame import Surface


class BladeAssets:
    def __init__(
            self,
            path: Path,
            grass_manager  # type: 'GrassManager'
    ) -> None:
        self.grass_manager = grass_manager  # type: 'GrassManager'

        # self.blades: list = support.import_folder_img(path)  # TODO: fix
        # self.blades = list(map(lambda img: img.set_colorkey((0, 0, 0)), self.blades))

        self.blades: list[Surface] = []

        # load in blade images
        for blade in sorted(os.listdir(path)):
            img: Surface = pg.image.load(path.joinpath(f'{blade}')).convert()
            img.set_colorkey((0, 0, 0))
            self.blades.append(img)

    def render_blade(self, surf: Surface, blade_id: int, location: tuple[float, float], rotation: int) -> None:
        # rotate the blade
        rot_img: Surface = pg.transform.rotate(self.blades[blade_id], rotation)

        # shade the blade of grass based on its rotation
        shade: Surface = pg.Surface(rot_img.get_size())
        shade_amount: float = self.grass_manager.shade_amount * (abs(rotation) / 90)
        shade.set_alpha(shade_amount)  # noqa
        rot_img.blit(shade, (0, 0))

        # render the blade
        half_width, half_height = rot_img.get_width() // 2, rot_img.get_height() // 2
        surf.blit(rot_img, (location[0] - half_width, location[1] - half_height))


