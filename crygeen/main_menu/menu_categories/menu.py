import math
import operator
from pathlib import Path
from typing import Callable

import pygame as pg
from pygame import Surface, Rect
from pygame.font import Font

from crygeen.main_menu.buttons import Button
from crygeen.settings import settings


class Menu:
    def __init__(self) -> None:
        # general setup _____________________________________________________________________________
        self.screen_size: tuple[int, int] = pg.display.get_window_size()

        # main_menu setup ________________________________________________________________________________
        self.font_name: Path = settings.MAIN_MENU_FONT
        self.font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR
        self.position: str = settings.MAIN_MENU_POSITION
        self._main_menu_list: dict = settings.MAIN_MENU_LIST
        self.alpha: int = settings.MAIN_MENU_ALPHA
        self.button_opacity_offset: float = settings.MAIN_MENU_BUTTON_OPACITY_OFFSET

        # main_menu buttons setup
        self.buttons_list: list = []
        self.y_dest_positions: list = []
        self.__create_menu_buttons()

        # dropdown main_menu effect
        self.dropdown_animation_time: int = settings.MAIN_MENU_DROPDOWN_ANIMATION
        self.dropdown_start_time: int = 0

        self.close_exit_menu: bool = False

    # main main_menu setup _______________________________________________________________________________
    def __create_menu_buttons(self) -> None:
        """
        Creates the main main_menu buttons and add them to the buttons list.
        Coordinates are set for the location of buttons on the screen.
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
                font_name=self.font_name,
                font_size=self.font_size,
                font_color=self.font_color,
                position=self.position,
                opacity_offset=self.button_opacity_offset,
                alpha=self.alpha,
                index=index,
                properties=self._main_menu_list[title]
            )
            self.y_dest_positions.append(dest_pos_y)
            self.buttons_list.append(button)
