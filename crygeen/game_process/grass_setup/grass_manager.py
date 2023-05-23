import math
import random
from copy import deepcopy
from pathlib import Path
from typing import Callable, Optional

from pygame import Surface

from crygeen.game_process.game_settings import gSettings
from crygeen.game_process.grass_setup.blade_assets import BladeAssets
from grass_manager import GrassTile


class GrassManager:
    """
    <grass_path>
    The only required argument. It points to the folder with all the blade images.
    the image names don't matter. When creating tiles, you need to provide a list of identifiers that
    are indexes of blade patterns that can be used. Indexes are based on alphabetical
    order, so img_01.png must be used instead of img_1.png to use two-digit numbers.
    Otherwise, img_10.png will come first.

    <_tile_size>
    This is used to define the "tile size" for the grass. Actual tile size should be some
    multiple of the number given here. This affects a couple of things. First, it defines the
    smallest section of grass that can be individually affected by efficient rotation modifications
    (such as wind). Second, it affects performance. If the size is too large, an unnecessary amount of
    calculations will be made for applied forces. If the size is too small, there will be too many
    images render, which will also reduce performance.

    <shade_amount>
    The shade amount determines the maximum amount of transparency that can be applied to a blade
    as it tilts away from its base angle. This should be a value from 0 to 255.

    <stiffness>
    This determines how fast the blades of grass bounce back into place after being rotated by an applied force.

    <_max_unique>
    This determines the maximum amount of variants that can be used for a specific tile configuration
    (a configuration is the combination of the amount of blades of grass and the possible set of blade
    images that can be used for a tile). If the number is too high, the application will use a
    large amount of RAM to store all the cached tile images. If the number is too low, the same
    patterns will start to appear.

    <place_range>
    This determines the vertical range that the base of the blades can be placed at. The range
    should be any range in the range of 0 to 1. [1, 1] to position the blades at the bottom of
    the tile. [0, 1] to place blades anywhere on the tile.

    <padding>
    This is the amount of spacial padding the tile images have to fit the blades spilling
    outside the bounds of the tile. Should be installed at the height of the tallest blade.
    """

    def __init__(self, grass_path: Path) -> None:
        self._blade_assets: BladeAssets = BladeAssets(grass_path, self)

        # caching
        self.grass_id: int = 0
        self.grass_cache: dict[tuple[int, int], Surface] = {}
        self.shadow_cache: dict[int, Surface] = {}
        self._formats: dict = {}  # too complex to paint

        # tile data
        self._grass_tiles: dict[tuple[int, int], GrassTile] = {}

        # config
        self._tile_size: int = gSettings.GRASS_TILE_SIZE
        self.shade_amount: int = gSettings.GRASS_SHADE_AMOUNT
        self.stiffness: int = gSettings.GRASS_STIFFNESS
        self._max_unique: int = gSettings.GRASS_MAX_UNIQUE
        self.vertical_place_range: list[float, float] = gSettings.GRASS_PLACE_RANGE
        self.ground_shadow: list[int, tuple[int, int, int], int, tuple[int, int]] = [0, (0, 0, 0), 100, (0, 0)]
        self.padding: int = gSettings.GRASS_PADDING

    def enable_ground_shadows(
            self,
            shadow_strength: int = gSettings.GRASS_SHADOW_STRENGTH,
            shadow_radius: int = gSettings.GRASS_SHADOW_RADIUS,
            shadow_color: tuple[int, int, int] = gSettings.GRASS_SHADOW_COLOR,
            shadow_shift: tuple[int, int] = gSettings.GRASS_SHADOW_SHIFT
    ) -> None:
        """
        Enables shadows for individual blades (or disables if shadow_strength is set to 0).
        shadow_radius determines the radius of the shadow circle, shadow_color determines
        the base color of the shadow, and shadow_shift is the offset of the shadow relative to
        the base of the blade.

        :param shadow_strength: Shading power
        :param shadow_radius: Shadow circle radius
        :param shadow_color: Shadow color
        :param shadow_shift: Shadow offset
        :return: None
        """
        if shadow_color == (0, 0, 0):
            shadow_color: tuple[int, int, int] = (0, 0, 1)
        self.ground_shadow: list[int, int, tuple[int, int, int], tuple[int, int]] = [
            shadow_radius, shadow_color, shadow_strength, shadow_shift
        ]

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
            return deepcopy(random.choice(self._formats[format_id]['data']))

        else:
            self._formats[format_id]['count'] += 1
            self._formats[format_id]['data'].append((tile_id, data))

    def place_tile(self, location: tuple[int, int] | list[int, int], density: int, grass_options: list[int]) -> None:
        """
        Adds new grass. location specifies which "tile" the grass should be placed at, so
        the pixel-position of the tile will depend on the GrassManager's tile size. density
        specifies the number of blades the tile should have and grass_options is a list of blade
        image IDs that can be used to form the grass tile. The blade image IDs are the alphabetical
        index of the image in the asset folder provided for the blades. Please note that you can
        specify the same ID multiple times in the grass options to make it more likely to appear.

        :param location: Where the grass should be placed
        :param density: The number of blades
        :param grass_options: A list of blade image IDs
        :return: None
        """
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
        """
        Applies a physical force to the grass at the given location. The radius is the range
        at which the grass should be fully bent over at. The force_drop_off is the distance past the
        end of the "radius" that it should take for the force to be eased into nothing.

        :param location: Where the force should be applied
        :param radius: The range at which the force should be applied
        :param force_drop_off: The distance past the end of the "radius" that it should take for
                               the force to be eased into nothing
        :return: None
        """
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
        """
        Renders the grass onto a surface and applies updates. Surf is the surface rendered
        onto, dt is the amount of seconds passed since the last update, offset is the camera's
        offset, and the rot_function is for custom rotational modifiers. The rot_function passed
        as an argument should take an X and Y value while returning a rotation value. Take a look
        at grass_demo.py to how you can create a wind effect with this.

        :param surf: Surface on which to draw grass
        :param dt: Time between current and last frame
        :param offset: Camera's offset
        :param rot_function: Pass a function that will be responsible for the animation of the grass
                            (rotation of the blades)
        :return: None
        """
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
                    surf, offset=(offset[0] - self.ground_shadow[3][0], offset[1] - self.ground_shadow[3][1])  # noqa
                )
        # render the grass tiles
        for pos in render_list:
            tile: GrassTile = self._grass_tiles[pos]
            tile.render(surf, dt, offset=offset)

            if rot_function:
                tile.set_rotation(rot_function(tile.loc[0], tile.loc[1]))
