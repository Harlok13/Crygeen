import math
import random
from typing import Optional

import pygame as pg
from pygame import Surface


class GrassTile:
    def __init__(
            self,
            tile_size: int,
            location: tuple[int, int],
            density: int,
            config: list[int],
            blade_assets,  # type: 'BladeAssets'
            grass_manager  # type: 'GrassManager'
    ) -> None:
        """

        :param tile_size: Size of one grass tile
        :param location: Grass tile location coordinates
        :param density: Grass density
        :param config: List of blades IDs
        :param blade_assets: Сlass responsible for initializing blade images
        :param grass_manager: Grass manipulation class
        """
        self._blade_assets = blade_assets  # type: 'BladeAssets'
        self._grass_manager = grass_manager  # type: 'GrassManager'

        self.loc: tuple[int, int] = location
        self._tile_size: int = tile_size
        self._master_rotation: int = 0
        self._precision: int = 30  # todo reloc to settings
        self._padding: int = self._grass_manager.padding
        self._increase: float = 90 / self._precision
        self._density: int = density
        self._config: list[int] = config

        self._blades: list[list[tuple[float, float], int, float]] = []
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
        self._custom_blade_data: Optional[list[Optional]] = None  # this is not correct typing

        self._render_data: Optional[tuple[int, int]] = None
        self._true_rotation: Optional[float] = None
        self.__update_render_data()

    def __generate_blade_data(self) -> None:
        y_range: float = self._grass_manager.vertical_place_range[1] - self._grass_manager.vertical_place_range[0]
        for i in range(self._density):
            new_blade: int = random.choice(self._config)
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
            self._base_id: int = overwrite[0]

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
            orig_data = self._custom_blade_data[index]  # save orig data
            distance: float = math.sqrt((self.loc[0] + blade[0][0] - force_point[0]) ** 2
                                        + (self.loc[1] + blade[0][1] - force_point[1]) ** 2)
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
        self._render_data: tuple[int, int] = (self._base_id, self._master_rotation)
        self._true_rotation: float = self._increase * self._master_rotation

    def set_rotation(self, rotation: int) -> None:
        self._master_rotation: int = rotation
        self.__update_render_data()

    def __render_tile(self, render_shadow: bool = False) -> Surface | tuple[Surface, Surface]:
        # make a new padded surface (to fit blades spilling out of the tile)
        surf: Surface = pg.Surface((self._tile_size + self._padding * 2, self._tile_size + self._padding * 2))
        surf.set_colorkey((0, 0, 0))

        # use custom_blade_data if its active (uncached), otherwise use the base data (cached).
        if self._custom_blade_data:
            blades: list = self._custom_blade_data
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
                blade[1],  # noqa
                (blade[0][0] + self._padding, blade[0][1] + self._padding),
                max(-90, min(90, blade[2] + self._true_rotation))  # noqa
            )

        # return surf and shadow_surf if applicable
        if render_shadow:
            return surf, shadow_surf  # noqa
        else:
            return surf

    def render_shadow(self, surf: Surface, offset: tuple[int, int] = (0, 0)) -> None:
        if self._grass_manager.ground_shadow[0] and (self._base_id in self._grass_manager.shadow_cache):
            surf.blit(
                self._grass_manager.shadow_cache[self._base_id],
                (self.loc[0] - offset[0] - self._padding, self.loc[1] - offset[1] - self._padding)
            )

    @staticmethod
    def __normalize(value: float, amount: float, target: float) -> float:
        if value > target + amount:
            value -= amount
        elif value < target - amount:
            value += amount
        else:
            value = target
        return value

    def render(self, surf: Surface, dt: float, offset: tuple[int, int]) -> None:
        # render a new grass tile image if using custom uncached data otherwise use cached data if possible
        if self._custom_blade_data:
            surf.blit(
                self.__render_tile(), (self.loc[0] - offset[0] - self._padding, self.loc[1] - offset[1] - self._padding)
            )
        # check if a new cached image needs to be generated and use the cached data if not (also cache shadow if necessary)
        else:
            # check needs to cache shadow also
            if (self._render_data not in self._grass_manager.grass_cache) and (
                    self._grass_manager.ground_shadow[0] and self._base_id not in self._grass_manager.shadow_cache):
                grass_img, shadow_img = self.__render_tile(render_shadow=True)
                self._grass_manager.grass_cache[self._render_data] = grass_img
                self._grass_manager.shadow_cache[self._base_id] = shadow_img
            elif self._render_data not in self._grass_manager.grass_cache:
                self._grass_manager.grass_cache[self._render_data] = self.__render_tile()

            # render image from the cache
            surf.blit(self._grass_manager.grass_cache[self._render_data],
                      (self.loc[0] - offset[0] - self._padding, self.loc[1] - offset[1] - self._padding))

        # attempt to move blades back to their base position
        if self._custom_blade_data:
            matching: bool = True
            for index, blade in enumerate(self._custom_blade_data):

                blade[2]: float = self.__normalize(
                    blade[2],
                    self._grass_manager.stiffness * dt,
                    self._blades[index][2]  # noqa
                )
                if blade[2] != self._blades[index][2]:
                    matching: bool = False

                # mark the data as non-custom once in base position so the cache ca be used
                if matching:
                    self._custom_blade_data = None
