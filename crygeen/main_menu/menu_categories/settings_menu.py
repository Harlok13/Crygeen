from pathlib import Path

import pygame as pg
from pygame import Surface

from crygeen.main_menu.buttons import LinkedList, Button, ControlButton
from crygeen.controls import Control, Key
from crygeen.main_menu.saver import SaveLoadManager
from crygeen.settings import settings


class SettingsMenu:
    def __init__(self, save_load_manager: SaveLoadManager) -> None:
        # general setup
        self._screen_size: tuple[int, int] = pg.display.get_window_size()
        self._save_load_manager: SaveLoadManager = save_load_manager

        # font setup
        self.font_name: Path = settings.MAIN_MENU_FONT
        self.font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR
        self.button_opacity_offset: int = settings.MAIN_MENU_BUTTON_OPACITY_OFFSET
        self.alpha: int = settings.MAIN_MENU_ALPHA

        # settings effects
        self.fade_surf: Surface = pg.Surface(self._screen_size)
        self.fade_surf.set_alpha(0)
        self.animation_start_time: int = 0
        self.alpha_vanish_duration: int = settings.SETTINGS_ALPHA_VANISH_DURATION
        self.start_alpha_vanish_opacity: int = settings.SETTINGS_START_ALPHA_VANISH_OPACITY
        self.end_alpha_vanish_opacity: int = settings.SETTINGS_END_ALPHA_VANISH_OPACITY
        self.control_dropdown_duration: int = settings.CONTROL_ANIMATION_DURATION

        # control buttons setup
        self.__control_data_path: Path = settings.CONTROL_DATA_PATH
        self.__control_data: list[list[str, int, str]] = self.__load_control_data()

        self.__linked_list: LinkedList = LinkedList()
        self.control_list: Control = settings.CONTROL
        self.buttons_list: list[Button] = []
        self.y_dest_positions: list[int] = []
        self.buttons_position: str = settings.CONTROL_BUTTONS_POSITION
        self._bottom_boundary: int = settings.CONTROL_BOTTOM_BOUNDARY
        self._top_boundary: int = settings.CONTROL_TOP_BOUNDARY
        self.scroll_offset: int = settings.CONTROL_SCROLL_OFFSET
        self.font_size: int = settings.CONTROL_FONT_SIZE
        self.control_x: int = settings.CONTROL_X
        self.control_y: int = settings.CONTROL_Y
        self.control_y_offset: int = settings.CONTROL_Y_OFFSET
        self.control_key_x: int = settings.CONTROL_KEY_X

        self.__create_settings_buttons()  # don't change the order
        self.control_close_y: list[int] = settings.CONTROL_CLOSE_Y * len(self.buttons_list)
        self.control_buttons_list: list[ControlButton] = [button.control_button for button in self.buttons_list]

    def __create_settings_buttons(self) -> None:
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
                    x=self.control_key_x,
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
            self.__linked_list.append(button)
            self.y_dest_positions.append(dest_pos_y)
            self.buttons_list.append(button)

        for button in self.buttons_list:
            button.surf.set_alpha(0)
            button.control_button.surf.set_alpha(0)

    def scroll_menu(self, event_key: int) -> None:
        """
        Check if the top and bottom button of the linked list is not outside the bottom and top
        boundary. If it is, the vertical offset is set to the provided scroll_offset.

        :param event_key: Key code.
        :return: None
        """
        if event_key == 4:
            if self.__linked_list.head.button.rect.y <= self._bottom_boundary:
                self.__linked_list.set_y_offset(self.scroll_offset)

        elif event_key == 5:
            if self.__linked_list.tail.button.rect.y >= self._top_boundary:
                self.__linked_list.set_y_offset(-self.scroll_offset)

    def __load_control_data(self) -> list[list[str, int, str]]:
        """
        Loads control data from the path "__control_data_path".
        If the file is not found, it writes the default "control_list" to the file and loads it again.

        :return: A list of lists, where each sub-list contains three elements: button title,
                 key value and key title.
        """
        try:
            return self._save_load_manager.load_save(self.__control_data_path)
        except FileNotFoundError:
            self._save_load_manager.write_save(self.control_list, self.__control_data_path)
            return self._save_load_manager.load_save(self.__control_data_path)
