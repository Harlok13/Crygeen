import math
import operator
from pathlib import Path
from typing import Callable

import pygame as pg
from pygame import Surface, Rect
from pygame.font import Font

from crygeen.main_menu.buttons import Button
from crygeen.main_menu.states import Status
from crygeen.settings import settings


class Menu:
    def __init__(self) -> None:
        # general setup
        self.screen_size: tuple[int, int] = pg.display.get_window_size()

        # font setup
        self.font_name: Path = settings.MAIN_MENU_FONT
        self.font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR

        # main_menu buttons setup
        self.button_opacity_offset: float = settings.MAIN_MENU_BUTTON_OPACITY_OFFSET
        self.position: str = settings.MAIN_MENU_POSITION
        self.alpha: int = settings.MAIN_MENU_ALPHA
        self._main_menu_list: dict[str, dict[str, str | Status]] = settings.MAIN_MENU_LIST
        self.buttons_list: list[Button] = []
        self.y_dest_positions: list[int] = []
        self.__create_menu_buttons()
        self.menu_close_y: list[int] = settings.MENU_CLOSE_Y * len(self.buttons_list)

        # dropdown main_menu effect
        self.dropdown_duration: int = settings.MAIN_MENU_DROPDOWN_DURATION
        self.animation_start_time: int = 0

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
