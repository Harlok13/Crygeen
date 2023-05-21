import math
import random
from copy import deepcopy
from pathlib import Path
from typing import Callable, Optional

import pygame as pg
from pygame import Surface

from crygeen.utils import support


class GrassManager:
    def __init__(
            self,
            grass_path: Path,
            tile_size: int = 15,
            shade_amount: int = 100,
            stiffness: int = 360,
            max_unique: int = 10,
            place_range: list[int, int] = [1, 1],  # noqa
            padding: int = 13  # todo add properties in settings
    ) -> None:
        self._blade_assets: BladeAssets = BladeAssets(grass_path, self)

        # caching
        self.grass_id: int = 0
        self._grass_cache: dict = {}
        self.shadow_cache: dict = {}
        self._formats: dict = {}

        # tile data
        self._grass_tiles: dict[tuple[int, int], GrassTile] = {}

        # config
        self._tile_size: int = tile_size
        self.shade_amount: int = shade_amount
        self._stiffness: int = stiffness
        self._max_unique: int = max_unique
        self.vertical_place_range: list[float, float] = place_range
        self.ground_shadow: list[int, tuple[int, int, int], int, tuple[int, int]] = [0, (0, 0, 0), 100, (0, 0)]
        self.padding: int = padding

    def enable_ground_shadows(  # todo reloc to api, add property in settings
            self,
            shadow_strength: int = 40,
            shadow_radius: int = 2,
            shadow_color: tuple[int, int, int] = (0, 0, 1),
            shadow_shift: tuple[int, int] = (0, 0)
    ) -> None:
        if shadow_color == (0, 0, 0):
            shadow_color: tuple[int, int, int] = (0, 0, 1)
        self.ground_shadow = [shadow_radius, shadow_color, shadow_strength, shadow_shift]

    def get_format(
            self,
            format_id: tuple[int, tuple[int, ...]],
            data: list[list[tuple[float, float], int, float]],
            tile_id: int
    ) -> Optional[tuple[int, list[list[float, int, float]]]]:
        if format_id not in self._formats:
            self._formats[format_id]: dict[str, int | list[tuple[int, list[list[tuple[float, float], int, float]]]]] = {
                'count': 1,
                'data': [(tile_id, data)]
            }

        elif self._formats[format_id]['count'] >= self._max_unique:
            print(deepcopy(random.choice(self._formats[format_id]['data'])))
            return deepcopy(random.choice(self._formats[format_id]['data']))

        else:
            self._formats[format_id]['count'] += 1
            self._formats[format_id]['data'].append((tile_id, data))

    def place_tile(self, location: tuple[int, int] | list[int, int], density: int, grass_options: list[int]) -> None:
        new_grass_loc: tuple[int, int] = tuple(location)
        if new_grass_loc not in self._grass_tiles:
            self._grass_tiles[new_grass_loc] = GrassTile(
                self._tile_size,
                (new_grass_loc[0] * self._tile_size, new_grass_loc[1] * self._tile_size),
                density,
                grass_options,
                self._blade_assets,
                self
            )

    def apply_force(self, location: tuple[int, int] | list[int, int], radius: float, force_drop_off: float) -> None:
        location: tuple[int, int] = tuple(map(int, location))  # type: ignore
        get_grid: Callable = lambda position: int(position) // self._tile_size
        grid_pos: tuple[int, int] = tuple(map(get_grid, location))  # type: ignore
        force_range: int = math.ceil((radius + force_drop_off) / self._tile_size)

        for y in range((diameter := force_range * 2) + 1):
            y -= force_range
            for x in range(diameter + 1):
                x -= force_range
                pos: tuple[int, int] = (grid_pos[0] + x, grid_pos[1] + y)
                if pos in self._grass_tiles:
                    self._grass_tiles[pos].apply_force(location, radius, force_drop_off)

    def update_render(
            self,
            surf: Surface,
            dt: float,
            offset: tuple[int, int] = (0, 0),
            rot_function: Callable = None
    ) -> None:
        visible_tile_range: tuple[int, int] = (int(surf.get_width() // self._tile_size) + 1,
                                               int(surf.get_height() // self._tile_size) + 1)
        base_pos: tuple[int, int] = (int(offset[0] // self._tile_size),
                                     int(offset[1] // self._tile_size))

        render_list: list[tuple[int, int]] = []
        for y in range(visible_tile_range[1]):
            for x in range(visible_tile_range[0]):
                pos: tuple[int, int] = (base_pos[0] + x, base_pos[1] + y)
                if pos in self._grass_tiles:
                    render_list.append(pos)

        # render shadow if applicable
        if self.ground_shadow[0]:
            for pos in render_list:
                self._grass_tiles[pos].render_shadow(
                    surf, offset=(offset[0] - self.ground_shadow[3][0], offset[1] - self.ground_shadow[3][1])
                )
        # render the grass tiles
        for pos in render_list:
            tile: GrassTile = self._grass_tiles[pos]
            tile.render(surf, dt, offset=offset)

            if rot_function:
                tile.set_rotation(rot_function(tile.loc[0], tile.loc[1]))


class GrassApi(GrassManager):
    def __init__(self) -> None:
        super().__init__(...)


class BladeAssets:
    def __init__(self, path: Path, gm: GrassManager) -> None:
        self.gm: GrassManager = gm
        self.blades: list = support.import_folder_img(path)

        self.blades = list(map(lambda img: img.set_colorkey((0, 0, 0)), self.blades))

    def render_blade(self, surf: Surface, blade_id: int, location: tuple[float, float], rotation: int) -> None:
        # rotate the blade
        rot_img: Surface = pg.transform.rotate(self.blades[blade_id], rotation)

        # shade the blade of grass based on its rotation
        shade: Surface = pg.Surface(rot_img.get_size())
        shade_amt: float = self.gm.shade_amount * (abs(rotation) / 90)
        shade.set_alpha(shade_amt)  # noqa
        rot_img.blit(shade, (0, 0))

        # render the blade
        half_width, half_height = rot_img.get_width() // 2, rot_img.get_height() // 2
        surf.blit(rot_img, (location[0] - half_width, location[1] - half_height))


class GrassTile:
    def __init__(
            self,
            tile_size: int,
            location: tuple[int, int],
            density: int,
            config,  # todo type
            blade_assets: BladeAssets,
            grass_manager: GrassManager
    ) -> None:
        self._blade_assets: BladeAssets = blade_assets
        self._grass_manager: GrassManager = grass_manager

        self.loc: tuple[int, int] = location
        self._tile_size: int = tile_size
        self._master_rotation: int = 0
        self._precision: int = 30  # todo reloc to settings
        self._padding: int = self._grass_manager.padding
        self._increase: float = 90 / self._precision
        self._density: int = density
        self._config: list[int] = config

        self._blades: list[list[tuple[float, float], int, float]] = []  # todo type
        self.__generate_blade_data()

        # layer back to front
        self._blades.sort(key=lambda x: x[1])

        # get next ID
        self._base_id: int = self._grass_manager.grass_id
        self._grass_manager.grass_id += 1

        self.__check_overwrite()

        """
        Custom blade_data is used when the blade's current state should not be cached. 
        All grass tiles will try to return to a cached state.
        """
        self._custom_blade_data: Optional[list[Optional]] = None  # todo type

        self._render_data: Optional[tuple[int, int]] = None
        self._true_rotation: Optional[float] = None
        self.__update_render_data()

    def __generate_blade_data(self) -> None:
        y_range: float = self._grass_manager.vertical_place_range[1] - self._grass_manager.vertical_place_range[0]
        for i in range(self._density):
            new_blade: int = random.choice(self._config)  # todo type
            y_pos: float = self._grass_manager.vertical_place_range[0]

            if y_range:
                y_pos: float = random.random() * y_range + self._grass_manager.vertical_place_range[0]

            self._blades.append([
                (random.random() * self._tile_size, y_pos * self._tile_size),
                new_blade,
                random.random() * 30 - 15  # todo settings
            ])

    def __check_overwrite(self) -> None:
        format_id: tuple[int, tuple[int, ...]] = (self._density, tuple(self._config))
        overwrite: Optional[tuple[int, list[list[tuple[float, float], int, float]]]] = self._grass_manager.get_format(
            format_id, self._blades, self._base_id
        )
        if overwrite:
            self._blades: list[list[tuple[float, float], int, float]] = overwrite[1]
            self.base_id: int = overwrite[0]

    def apply_force(self, force_point: tuple[int, int], force_radius: float, force_drop_off: float) -> None:
        """
        Applies a force to the object.

        The method applies the force to each blade of the object based on its distance
        from the force_point. The force drops off as the distance from the force_point
        increases. The direction of the force is determined based on the position of
        force_point relative to the leftmost blade. The direction of rotation of the
        object is updated only if the new force is greater than the previous force.

        :param force_point: A tuple containing the X and Y coordinates of the point where the force is applied.
        :param force_radius: The radius of the area in which the force is applied around the force_point.
        :param force_drop_off: The distance at which the force starts to decrease in strength from the force_point.
        :return: None
        """
        if not self._custom_blade_data:
            self._custom_blade_data: list[Optional] = [None] * len(self._blades)

        for index, blade in enumerate(self._blades):
            orig_data = self._custom_blade_data[index]  # todo make best
            distance: float = math.sqrt((self.loc[0] + blade[0][0] - force_point[0]) ** 2
                                        + (self.loc[1] + blade[0][1] - force_point[1]))
            max_force: bool = False

            if distance < force_radius:
                force: int = 2  # todo settings
            else:
                distance: float = max(0, distance - force_radius)  # noqa
                force: float = 1 - min(distance / force_drop_off, 1)

            direction: int = 1 if force_point[0] > (self.loc[0] + blade[0][0]) else -1

            if not self._custom_blade_data[index] or abs(
                    self._custom_blade_data[index][2] - self._blades[index][2]
            ) <= abs(force) * 90:  # todo settings

                self._custom_blade_data[index] = [
                    blade[0], blade[1], blade[2] + direction * force * 90  # noqa someday Ill understand what u want
                ]                                                          # but not today

    def __update_render_data(self) -> None:
        self._render_data: tuple[int, int] = (self.base_id, self._master_rotation)
        self._true_rotation: float = self._increase * self._master_rotation

    def set_rotation(self, rotation: int) -> None:
        self._master_rotation: int = rotation
        self.__update_render_data()

    def __render_tile(self, render_shadow: bool = False) -> None:
        # make a new padded surface (to fit blades spilling out of the tile)
        surf: Surface = pg.Surface((self._tile_size + self._padding * 2, self._tile_size + self._padding * 2))
        surf.set_colorkey((0, 0, 0))

        # use custom_blade_data if its active (uncached), otherwise use the base data (cached).
        if self._custom_blade_data:
            blades = self._custom_blade_data  # todo type
        else:
            blades: list[list[tuple[float, float], int, float]] = self._blades

        # render the shadows of each blade if applicable
        if render_shadow:
            shadow_surf: Surface = pg.Surface(surf.get_size())
            shadow_surf.set_colorkey((0, 0, 0))
            for blade in self._blades:
                pg.draw.circle(
                    shadow_surf,
                    self._grass_manager.ground_shadow[1],
                    (blade[0][0] + self._padding, blade[0][1] + self._padding),
                    self._grass_manager.ground_shadow[0]
                )
            shadow_surf.set_alpha(self._grass_manager.ground_shadow[2])

        # render each blade using the asset manager
        for blade in blades:
            self._blade_assets.render_blade(
                surf,
                blade[1],
                (blade[0][0] + self._padding, blade[0][1] + self._padding),
                max(-90, min(90, blade[2] + self._true_rotation))
            )

        # return surf and shadow_surf if applicable
        if render_shadow:
            return surf, shadow_surf
        else:
            return surf

    def render_shadow(self, surf: Surface, offset: tuple[int, int] = (0, 0)) -> None:
        if self._grass_manager.ground_shadow[0] and (self._base_id in self._grass_manager.shadow_cache):
            surf.blit(self._grass_manager.shadow_cache[self.base_id], )
