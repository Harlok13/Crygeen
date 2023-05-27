import math
import operator
from typing import Callable

import pygame as pg
from pygame import Surface, Rect
from pygame.font import Font

from crygeen.main_menu.buttons import Button
from crygeen.main_menu.saver import SaveLoadManager
from crygeen.settings import settings
from crygeen.main_menu.states import Status


class Menu:
    def __init__(self) -> None:
        # general setup _____________________________________________________________________________
        self._display_surface: Surface = pg.display.get_surface()
        self._screen_size: tuple[int, int] = self._display_surface.get_size()
        self.save_load_manager: SaveLoadManager = SaveLoadManager()

        # menu setup ________________________________________________________________________________
        self.main_menu_font_name: str = settings.MAIN_MENU_FONT
        self.main_menu_font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.main_menu_font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR
        self.main_menu_position: str = settings.MAIN_MENU_POSITION
        self._main_menu_list: dict = settings.MAIN_MENU_LIST
        self.alpha: int = settings.MAIN_MENU_ALPHA
        self.button_opacity_offset: float = settings.MAIN_MENU_BUTTON_OPACITY_OFFSET

        # menu buttons setup
        self.menu_buttons_list: list = []
        self._menu_y_dest_positions: list = []
        self.__create_menu_buttons()

        # dropdown menu effect
        self.dropdown_animation_time: int = settings.MAIN_MENU_DROPDOWN_ANIMATION
        self.dropdown_start_time: int = 0

        # garbage ___________________________________________________________________________________
        self.img = pg.image.load(
            settings.BASE_PATH.joinpath('assets', 'graphics', 'settings', 'setting_bg6.jpeg')).convert_alpha()

    # supporting functions __________________________________________________________________________
    def _alpha_vanish(
            self,
            duration: int,
            start_time: int,
            start_alpha: int,
            end_alpha: int,
            surface: Surface,
            color: str | tuple = settings.SCREENSAVER_SURF_COLOR,
    ) -> None:
        """
        Used to fade the screen in and out by adjusting the alpha value of a
        shading surface. If 'reverse' is set to 'True', then the screen fades
        out, otherwise it fades in. The 'offset' parameter determines how quickly
        the shading fades, and 'color' determines the color of the shading.
        :param duration: Animation play time.
        :param start_time: The time at which the screen should start fading.
        :param color: A string or tuple representing the color of the shading surface.
                      Default value is 'settings.SCREENSAVER_ALPHA_COLOR'.
        :param reverse: A boolean value indicating whether the screen should fade out
                        ('True') or fade in ('False'). Default value is 'False'.
        :return:  # TODO ref doc
        """
        op: Callable = (operator.lt, operator.gt)[start_alpha > end_alpha]

        surface.fill(color)
        delta: int = pg.time.get_ticks() - start_time
        erp_alpha: float = self._lerp(start_alpha, end_alpha, delta / duration)
        if op(erp_alpha, end_alpha):  # < or >
            surface.set_alpha(erp_alpha)  # type: ignore
        self._display_surface.blit(surface, (0, 0))

    def _dropdown_menu_effect(
            self,
            buttons_list: list[Button],
            start_time: int,
            animation_time: int,
            y_dest_positions: list[int],
            shading: bool = False
    ) -> None:
        """
        Play animation, when open menu.
        self.dropdown_animation_time: The duration of the animation.
        delta: The time elapsed since the function was called.
        :return:
        """
        opacity_values = (self.alpha, 0) if shading else (0, self.alpha)
        if animation_time > 0:
            delta: int = pg.time.get_ticks() - start_time
            for button in buttons_list:
                if delta < animation_time:
                    button.rect.y = self._lerp(
                        button.rect.y, y_dest_positions[button.index], delta / animation_time
                    )
                    button.surf.set_alpha(self._lerp(
                        *opacity_values, delta / animation_time
                    ))

    @staticmethod
    def _lerp(a: float, b: float, t: float) -> float | int:
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
    def _add_text_effect(obj: Surface):
        item_alpha: int = int(abs(math.sin(pg.time.get_ticks() / 1000)) * 128 + 128)
        obj.set_alpha(item_alpha)

    def _draw_text(self, text: str, font: Font, x: int, y: int) -> tuple[Rect, Surface]:
        """
        Draw a text on the screen.
        :param text: The text to be displayed.
        :param font: The font used for the text.
        :param surface: The Surface object on which the text will be drawn.
        :param x: The x-coordinate of the starting point of text display.
        :param y: The y-coordinate of the starting point of text display.
        :param emergence: If the text should be smoothly emerging.
        :param text_effect: If the text should be animated.
        :return:
        """
        text_obj: Surface = font.render(text, True, self.main_menu_font_color)
        text_rect: Rect = text_obj.get_rect()
        text_rect.center = (x, y)

        return text_rect, text_obj

    # main menu setup _______________________________________________________________________________
    def __create_menu_buttons(self) -> None:
        """
        Creates the main menu buttons and add them to the buttons list.
        Сoords are set for the location of buttons on the screen.
        :return:
        """
        x: int = settings.MAIN_MENU_X
        y, y_offset = settings.MAIN_MENU_Y, settings.MAIN_MENU_Y_OFFSET
        dest_pos_y = y
        for index, title in enumerate(self._main_menu_list):
            dest_pos_y += y_offset
            button: Button = Button(
                title=title,
                x=x,
                y=y,
                font_name=self.main_menu_font_name,
                font_size=self.main_menu_font_size,
                font_color=self.main_menu_font_color,
                position=self.main_menu_position,
                opacity_offset=self.button_opacity_offset,
                alpha=self.alpha,
                index=index,
                properties=self._main_menu_list[title]
            )
            self._menu_y_dest_positions.append(dest_pos_y)
            self.menu_buttons_list.append(button)

    def display_menu(self, status: Status, exit_menu, settings_menu):
        """
        Displays menu buttons on the screen based on the application state.
        If the application status is 'Status.MAIN_MENU', the method starts the menu
        animation and displays all menu buttons. If the mouse is hovering
        over a button, it "fades in" using the 'fade_in_hover' method,
        otherwise it returns to its original value.
        :return:
        """
        if status == Status.MAIN_MENU:
            self._dropdown_menu_effect(
                self.menu_buttons_list, self.dropdown_start_time, self.dropdown_animation_time,
                self._menu_y_dest_positions
            )
        if status != Status.MAIN_MENU:
            self._dropdown_menu_effect(
                self.menu_buttons_list, exit_menu.exit_dropdown_start_time, self.dropdown_animation_time,
                [1000] * len(self.menu_buttons_list), True
            )  # TODO ref hard code

        for button in self.menu_buttons_list:
            button.fade_in_hover()

            self._display_surface.blit(button.surf, button.rect)
