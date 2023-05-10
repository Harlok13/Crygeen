import math
import operator
import random
from pathlib import Path
from typing import Optional, Callable

import pygame as pg
import pygame.freetype
from pygame import Surface, Rect
from pygame.font import Font
from pygame.mixer import Sound

from crygeen import audio
from crygeen.buttons import Button, LinkedList
from crygeen.controls import Key
from crygeen.settings import settings
from crygeen.states import Status
from crygeen.support import import_folder_img


class Menu:
    def __init__(self) -> None:
        # general setup _____________________________________________________________________________
        self._display_surface: Surface = pg.display.get_surface()
        self._screen_size: tuple[int, int] = self._display_surface.get_size()

        # menu setup ________________________________________________________________________________
        self.main_menu_font_name: str = settings.MAIN_MENU_FONT
        self.main_menu_font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.main_menu_font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR
        self.main_menu_position: str = settings.MAIN_MENU_POSITION
        self._main_menu_list = settings.MAIN_MENU_LIST
        self.alpha: int = settings.MAIN_MENU_ALPHA
        self.button_opacity_offset: float = settings.MAIN_MENU_BUTTON_OPACITY_OFFSET

        # menu buttons setup
        self.menu_buttons_list: list = []
        self._menu_y_dest_positions: list = []
        self.__create_menu_buttons()

        # dropdown menu effect
        self.dropdown_animation_time = settings.MAIN_MENU_DROPDOWN_ANIMATION
        self.dropdown_start_time: int = 0

        # main theme setup __________________________________________________________________________
        self._music: bool = False
        self._main_sound: Sound = self.__set_menu_music()

        # garbage ___________________________________________________________________________________
        self.img = pg.image.load('setting_bg6.jpeg').convert_alpha()

    # supporting functions __________________________________________________________________________
    def __alpha_vanish(
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
        erp_alpha: float = self.__lerp(start_alpha, end_alpha, delta / duration)
        if op(erp_alpha, end_alpha):  # < or >
            surface.set_alpha(erp_alpha)  # type: ignore
        self._display_surface.blit(surface, (0, 0))

    def __dropdown_menu_effect(
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
                    button.rect.y = self.__lerp(
                        button.rect.y, y_dest_positions[button.index], delta / animation_time
                    )
                    button.surf.set_alpha(self.__lerp(
                        *opacity_values, delta / animation_time
                    ))

    def __draw_text(
            self,
            text: str,
            font: pygame.freetype.Font | Font,
            surface: Surface,
            x: int,
            y: int,
            emergence: bool = False,
            alpha_values: Optional[tuple[int, int]] = None,
            emergence_duration: Optional[int] = None,
            text_effect: bool = False
    ) -> tuple[Rect, Surface]:
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
    def __add_text_effect(obj: Surface):
        item_alpha: int = int(abs(math.sin(pg.time.get_ticks() / 1000)) * 128 + 128)
        obj.set_alpha(item_alpha)

    # music setup __________________________________________________________________________________
    def toggle_music(self, forcibly_set: Optional[bool] = None) -> None:
        """
        API for toggle music.
        If the argument is not specified, then the value is reversed,
        otherwise the value takes the value of the argument
        :param forcibly_set: If you need to get a specific value.
        :return:
        """
        self._main_sound: bool = (not self._music, forcibly_set)[bool(forcibly_set)]

    @staticmethod
    def __set_menu_music() -> Sound:
        """
        General setup music.
        Select one of the songs, set the volume and repeat cycle.
        :return: One random music in playlist.
        """
        main_sound: Sound = pg.mixer.Sound(random.choice(audio.MAIN_MENU_SOUND))
        main_sound.set_volume(audio.MAIN_MENU_VOLUME)
        main_sound.play(loops=audio.MAIN_MENU_LOOPS)
        return main_sound

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

    def __display_menu_buttons(self, status: Status):
        """
        Displays menu buttons on the screen based on the application state.
        If the application status is 'Status.MAIN_MENU', the method starts the menu
        animation and displays all menu buttons. If the mouse is hovering
        over a button, it "fades in" using the 'fade_in_hover' method,
        otherwise it returns to its original value.
        :return:
        """
        if status == status.MAIN_MENU:
            self.__dropdown_menu_effect(
                self.menu_buttons_list, self.dropdown_start_time, self.dropdown_animation_time,
                self._menu_y_dest_positions
            )
        if status != status.MAIN_MENU:
            self.__dropdown_menu_effect(
                self.menu_buttons_list, self.exit_dropdown_start_time, self.dropdown_animation_time,
                [1000] * len(self.menu_buttons_list), True
            )  # TODO ref hard code

        for button in self.menu_buttons_list:
            button.fade_in_hover()

            self._display_surface.blit(button.surf, button.rect)

    # run on main loop ______________________________________________________________________________
    def run(self, status: Status) -> None:
        """
        Run menu im main loop.
        :param status: Current status.
        :return:
        """
        self.__start_screensaver(status)
        if status != Status.SCREENSAVER:
            self.__display_menu_buttons(status)
        if status == Status.EXIT:
            self.__display_exit_menu()
        elif status == Status.SETTINGS:
            self.__display_settings_menu(status)
