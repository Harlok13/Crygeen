import math
import operator
from functools import wraps
from typing import Callable

import pygame as pg
from pygame import Surface, Rect
from pygame.font import Font

from crygeen.main_menu.buttons import Button, ControlButton
from crygeen.settings import settings
from crygeen.utils.support import deprecated


class MenuAnimation:
    @staticmethod
    def screensaver_text_effect(
            alpha_values: tuple[int, int], emergence_duration: int, end_alpha_opacity: int, wave: bool, start_time: int,
    ) -> Callable:
        """
        Calculates the alpha value of the text based on the starting and ending
        values and the duration of emergence. Then it adjusts the alpha value of
        the text surface based on the current time delta and duration of the emergence.
        Finally, the method returns the adjusted text surface and rect object.

        :param alpha_values: Representing the starting and ending alpha values for the text surface.
        :param emergence_duration: Duration of the text emergence effect in milliseconds.
        :param end_alpha_opacity: The ending alpha opacity of the text surface.
        :param wave: That determines whether to apply a wave effect to the text surface.
        :param start_time: The time (in milliseconds) at which the text effect begins.
        :return: The adjusted text surface and rect object.
        """
        def outer_wrapper(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> tuple[Surface, Rect]:

                text_surf, text_rect = func(*args, **kwargs)

                delta: int = pg.time.get_ticks() - start_time
                start_alpha, end_alpha = alpha_values
                dt: float = delta / emergence_duration
                alpha_offset: float | int = start_alpha + (end_alpha - start_alpha) * dt

                if alpha_offset <= end_alpha_opacity:
                    text_surf.set_alpha(alpha_offset)

                else:

                    if wave:
                        wave_alpha: int = int(abs(math.sin(pg.time.get_ticks() / 1000)) * 128 + 128)
                        text_surf.set_alpha(wave_alpha)

                    else:
                        text_surf.set_alpha(end_alpha_opacity)

                return text_surf, text_rect

            return wrapper

        return outer_wrapper

    def alpha_vanish(
            self,
            duration: int,
            start_alpha: int,
            end_alpha: int,
            fade_surface: Surface,
            canvas: Surface,
            start_time: int,
    ) -> None:
        """
        The function uses operators to determine if the fade is increasing
        or decreasing and fills the fade surface with a color specified in settings.
        The function uses time to calculate the elapsed time for the fade and uses
        linear interpolation to calculate the alpha value of the faded surface. The
        alpha value is then set using the set_alpha method and the faded surface is
        then blitted to the canvas.

        :param duration: An integer representing the time, in milliseconds, for the fade to complete.
        :param start_alpha: An integer representing the starting alpha value for the fade.
        :param end_alpha: An integer representing the ending alpha value for the fade.
        :param fade_surface: A Surface object that will be faded.
        :param canvas: A Surface object to which the faded surface will be blitted.
        :param start_time: An integer representing the time, in milliseconds, that the fade began.
        :return: None
        """
        op: Callable = (operator.lt, operator.gt)[start_alpha > end_alpha]

        fade_surface.fill(settings.SCREENSAVER_FADE_SURF_COLOR)

        delta: int = pg.time.get_ticks() - start_time
        erp_alpha: float = self.__lerp(start_alpha, end_alpha, delta / duration)

        if op(erp_alpha, end_alpha):  # < or >
            fade_surface.set_alpha(erp_alpha)  # type: ignore

        canvas.blit(fade_surface, (0, 0))

    def dropdown_menu_effect(
            self,
            buttons_list: list[Button],
            animation_duration: int,
            y_dest_positions: list[int],
            shading: bool,
            start_time: int
    ) -> None:
        """
        Plays an animation when the main menu is opened.
        The method uses opacity values of 128 and 0 (if shading is True)
        or 0 and 128 (if shading is False) and checks if the animation duration
        is greater than 0. It then calculates the delta time and updates the
        position and alpha values of each button using the linear interpolation
        method __lerp().

        :param buttons_list: The buttons in the dropdown menu.
        :param animation_duration: An integer that specifies the duration of the animation, in milliseconds.
        :param y_dest_positions: A list of integers that specify the destination y-coordinates of
                                 each button in the dropdown
        :param shading: A boolean flag that indicates whether shading should be applied to the buttons.
        :param start_time: An integer that represents the start time of the animation, in milliseconds since
                           the start of the program.
        :return: None
        """
        opacity_values = (128, 0) if shading else (0, 128)

        if animation_duration > 0:
            delta: int = pg.time.get_ticks() - start_time

            for button in buttons_list:
                if delta < animation_duration:
                    button.rect.y = self.__lerp(
                        button.rect.y, y_dest_positions[button.index], delta / animation_duration
                    )
                    button.surf.set_alpha(self.__lerp(
                        *opacity_values, delta / animation_duration
                    ))

    @staticmethod
    def __lerp(a: float, b: float, t: float) -> float | int:
        """
        Linear interpolation formula.
        The formula is used to smoothly change the start and end values of
        coordinates, and modify this value based on the time 't' elapsed
        since the start of the movement.
        :param a: The starting value.
        :param b: The ending value.
        :param t: The interpolation factor, ranging from 0 to 1.
        :return: The interpolated value between a and b based on the factor 't'.
        """
        return a + (b - a) * t

    @staticmethod
    @deprecated
    def _add_text_effect(obj: Surface) -> None:
        item_alpha: int = int(abs(math.sin(pg.time.get_ticks() / 1000)) * 128 + 128)
        obj.set_alpha(item_alpha)

    @staticmethod
    def draw_text(
            text: str, font: Font, x: int, y: int, font_color: tuple = settings.MAIN_MENU_FONT_COLOR
    ) -> tuple[Surface, Rect]:
        """
        Can be used to draw text onto a pygame surface with specified font and color,
        and centered at a particular coordinate.

        :param text: A string representing the text to be rendered on the surface
        :param font: The font to be used for rendering.
        :param x: The x-coordinate of the center of the rendered text rectangle.
        :param y: The y-coordinate of the center of the rendered text rectangle.
        :param font_color: An optional tuple specifying the color of the rendered text.
        :return: Tuple with text surface and rect.
        """
        text_surf: Surface = font.render(text, True, font_color)
        text_rect: Rect = text_surf.get_rect()
        text_rect.center = (x, y)

        return text_surf, text_rect,
