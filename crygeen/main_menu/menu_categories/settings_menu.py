from pathlib import Path

import pygame as pg
from pygame import Surface

from crygeen.main_menu.buttons import LinkedList, Button, ControlButton
from crygeen.controls import Control, Key
from crygeen.main_menu.saver import SaveLoadManager
from crygeen.settings import settings


class SettingsMenu:
    def __init__(self, save_load_manager: SaveLoadManager) -> None:
        self.screen_size: tuple[int, int] = pg.display.get_window_size()
        self.save_load_manager: SaveLoadManager = save_load_manager

        self.linked_list: LinkedList = LinkedList()
        self.control_list: Control = settings.CONTROL
        self.buttons_list: list = []
        self.y_dest_positions: list = []
        self.buttons_position: str = settings.CONTROL_BUTTONS_POSITION
        self.bottom_boundary: int = settings.CONTROL_BOTTOM_BOUNDARY
        self.top_boundary: int = settings.CONTROL_TOP_BOUNDARY
        self.scroll_offset: int = settings.CONTROL_SCROLL_OFFSET
        self.font_size: int = settings.CONTROL_FONT_SIZE
        self.control_x: int = settings.CONTROL_X
        self.control_y: int = settings.CONTROL_Y
        self.control_y_offset: int = settings.CONTROL_Y_OFFSET

        self.font_name: Path = settings.MAIN_MENU_FONT
        self.font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR
        self.button_opacity_offset: int = settings.MAIN_MENU_BUTTON_OPACITY_OFFSET
        self.alpha: int = settings.MAIN_MENU_ALPHA

        # settings effects
        self.fade_surf: Surface = pg.Surface(self.screen_size)
        self.fade_surf.set_alpha(0)
        self.dropdown_start_time: int = 0
        self.alpha_vanish_duration = settings.SETTINGS_ALPHA_VANISH_DURATION
        self.dest_alpha_vanish: int = settings.SETTINGS_DEST_ALPHA_VANISH
        self.control_animation_duration: int = settings.CONTROL_ANIMATION_DURATION

        # control buttons
        self.control_data_path: Path = settings.CONTROL_DATA_PATH
        self.__control_data: list[list[str, int, str]] = self.__load_control_data()

        self.__create_settings_buttons()

    def __create_settings_buttons(self) -> None:  # TODO remove code duplications
        # params: return tuple with buttons and dest pos
        x: int = self.control_x
        y, y_offset = self.control_y, self.control_y_offset
        dest_pos_y: int = y

        for index, key in enumerate(self.control_list):
            key: Key
            dest_pos_y += y_offset
            button_kwargs = {
                "title": f"{key.title}",
                "x": x,
                "y": y,
                "font_name": self.font_name,
                "font_size": self.font_size,
                "font_color": self.font_color,
                "position": self.buttons_position,
                "opacity_offset": self.button_opacity_offset,
                "alpha": self.alpha,
                "index": index,
                "properties": "",
            }
            button: Button = Button(
                **button_kwargs,
                control_button=ControlButton(
                    title=f"{self.__control_data[index][2]}",
                    x=1000,  # todo ref
                    y=y,
                    font_name=self.font_name,
                    font_size=self.font_size,
                    font_color=self.font_color,
                    position=self.buttons_position,
                    opacity_offset=self.button_opacity_offset,
                    alpha=self.alpha,
                    index=index,
                    properties="",
                    constant=self.__control_data[index][1],  # type: ignore
                    key=self.__control_data[index][2],
                )
            )
            self.linked_list.append(button)
            self.y_dest_positions.append(dest_pos_y)
            self.buttons_list.append(button)

    def scroll_menu(self, event_key: int) -> None:
        if event_key == 4:
            if self.linked_list.head.button.rect.y <= self.bottom_boundary:
                self.linked_list.set_y_offset(self.scroll_offset)

        elif event_key == 5:
            if self.linked_list.tail.button.rect.y >= self.top_boundary:
                self.linked_list.set_y_offset(-self.scroll_offset)

    def __load_control_data(self) -> list[list[str, int, str]]:
        try:
            return self.save_load_manager.load_save(self.control_data_path)
        except FileNotFoundError:
            self.save_load_manager.write_save(self.control_list, self.control_data_path)
            return self.save_load_manager.load_save(self.control_data_path)

