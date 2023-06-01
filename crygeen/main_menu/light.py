import math
import random

import pygame as pg
from pygame import Surface


class Light:
    """
    Holds the attributes for the light and offers some basic interface instructions.
    """

    def __init__(
        self,
        pos: list[int],
        radius: int,
        light_img: Surface,
        color: tuple[int, int, int] = (255, 255, 255),
        alpha: int = 255,
    ):
        self._base_position: list[int] = pos  # screen position
        self.position: list[int] = pos
        self._base_radius: int = radius  # screen size
        self.radius: int = radius
        self._base_light_img: Surface = pg.transform.scale(light_img, (radius * 2, radius * 2))
        self._colored_light_img: Surface = self._base_light_img.copy()
        self.light_img: Surface = self._base_light_img.copy()
        self.alpha: int = alpha
        self.color: tuple[int, int, int] = color
        self.timer: int = 1  # timer for wave/pule of light
        self.flicker_timer: int = 1  # timer for jumping flicker
        self.variance = 0  # how much variance from radius due to flicker
        self.variance_size = int(self._base_radius / 30)

        self._calculate_light_img()

    def update(self):
        base_radius = self._base_radius
        variance_size = self.variance_size

        # increment wave timer
        self.timer += 1
        self.set_size(int((1 + math.sin(self.timer / 10)) + (base_radius + self.variance)))

        # decrement flicker timer
        self.flicker_timer -= 1

        # update for flickering effect
        if self.flicker_timer < 0:
            # scale size
            self.variance = random.randint(-variance_size, variance_size)
            radius = base_radius + self.variance
            self.set_size(radius)

            # alpha variance
            alpha_variance = int(self.variance)
            self.set_alpha(max(0, min(255, self.alpha + alpha_variance)))

            # set new timer
            self.flicker_timer = random.randint(30, 60)

    def _calculate_light_img(self):
        """
        Alter the original light image by all of the attributes given, e.g. alpha, color, etc.
        """
        self._colored_light_img = mult_color(set_mask_alpha(self._base_light_img, self.alpha), self.color)
        self.light_img = self._colored_light_img.copy()

    def set_alpha(self, alpha: int):
        """
        Set the alpha value of the light. Refreshes the mask and size.
        """
        self.alpha = alpha
        self._colored_light_img = set_mask_alpha(self._base_light_img, self.alpha)
        self.set_size(self.radius)

    def set_color(self, color: tuple[int, int, int], override_alpha: bool = False):
        """
        Set the color of the light. Refreshes the size. If `override_alpha` is set to `True`, the alpha setting is
        ignored when recalculating the light. This is better for performance.
        """
        self.color = color
        if override_alpha:
            self._colored_light_img = mult_color(self._base_light_img, self.color)
        else:
            self._calculate_light_img()
        self.set_size(self.radius)

    def set_size(self, radius: int):
        """
        Set the size of the light and rescale the image to match.
        """
        self.radius = radius
        self.light_img = pg.transform.scale(self._colored_light_img, (radius * 2, radius * 2))


def set_mask_alpha(surf: Surface, alpha: int) -> Surface:
    """
    Set the alpha of the screen mask
    """
    return mult_color(surf, (alpha, alpha, alpha))


def mult_color(surf: Surface, color: tuple[int, int, int]) -> Surface:
    """
    Multiply the color given on the provided surface.
    """
    mult_surf = surf.copy()
    mult_surf.fill(color)
    new_surf = surf.copy()
    new_surf.blit(mult_surf, (0, 0), special_flags=BLEND_RGBA_MULT)
    return new_surf
