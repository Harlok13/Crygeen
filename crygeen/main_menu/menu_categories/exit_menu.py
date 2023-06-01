from pathlib import Path

import pygame as pg
from pygame import Surface
from pygame.font import Font

from crygeen.main_menu.buttons import Button
from crygeen.main_menu.states import Status
from crygeen.settings import settings


class ExitMenu:
    def __init__(self) -> None:
        # general setup
        self.buttons_list: list[Button] = []
        self.exit_list: dict[str, dict[str, Status | str]] = settings.EXIT_LIST
        self.screen_size: tuple[int, int] = pg.display.get_window_size()

        # animation setup
        self.animation_start_time: int = 0
        self.fade_surf: Surface = pg.Surface(self.screen_size)
        self.start_alpha_vanish_opacity: int = settings.EXIT_START_ALPHA_VANISH_OPACITY
        self.end_alpha_vanish_opacity: int = settings.EXIT_END_ALPHA_VANISH_OPACITY
        self.alpha_vanish_duration: int = settings.EXIT_ALPHA_VANISH_DURATION
        self.dropdown_duration: int = settings.EXIT_DROPDOWN_DURATION
        # text animation
        self.text_alpha_duration: int = settings.EXIT_TEXT_ALPHA_DURATION
        self.text_alpha: tuple[int, int] = settings.EXIT_TEXT_ALPHA
        self.text_end_alpha: int = settings.EXIT_TEXT_END_ALPHA

        # font setup
        self.font_name: Path = settings.MAIN_MENU_FONT
        self.font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR
        self.alpha: int = settings.MAIN_MENU_ALPHA
        self.button_opacity_offset: float = settings.MAIN_MENU_BUTTON_OPACITY_OFFSET

        # exit text setup
        self.text: str = settings.EXIT_TEXT
        self.text_x: int = settings.EXIT_TEXT_X
        self.text_y: int = settings.EXIT_TEXT_Y
        self.font: Font = pg.font.Font(settings.MAIN_MENU_FONT, settings.MAIN_MENU_FONT_SIZE)

        # exit buttons setup
        self.button_x: tuple[int, int] = settings.EXIT_BUTTON_X
        self.button_start_y: int = settings.EXIT_BUTTON_START_Y
        self.button_dest_y: list[int] = settings.EXIT_BUTTON_DEST_Y
        self.button_position: str = settings.EXIT_BUTTON_POSITION
        self.__create_exit_buttons()
        self.exit_close_y: list[int] = settings.EXIT_CLOSE_Y * len(self.buttons_list)

    def __create_exit_buttons(self) -> None:
        y: int = self.button_start_y
        x_coords: tuple[int, int] = self.button_x
        for index, title in enumerate(self.exit_list):
            button: Button = Button(
                title=title,
                x=x_coords[index],
                y=y,
                font_name=self.font_name,
                font_size=self.font_size,
                font_color=self.font_color,
                position=self.button_position,
                opacity_offset=self.button_opacity_offset,
                alpha=self.alpha,
                index=index,
                properties=self.exit_list[title]
            )
            self.buttons_list.append(button)

    def exit_button_action(self, key: int) -> Status:
        match key:
            case pg.K_RETURN:
                pg.quit()
                exit()
            case pg.K_ESCAPE:
                self.animation_start_time = pg.time.get_ticks()
                return Status.MAIN_MENU
