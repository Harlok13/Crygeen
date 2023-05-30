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

        self.font_name: Path = settings.MAIN_MENU_FONT
        self.font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR
        self.button_opacity_offset: int = settings.MAIN_MENU_BUTTON_OPACITY_OFFSET
        self.alpha: int = settings.MAIN_MENU_ALPHA

        # settings effects
        self.settings_fade_surf: Surface = pg.Surface(self.screen_size)
        self.settings_fade_surf.set_alpha(0)
        self.settings_dropdown_start_time: int = 0
        self._settings_alpha_vanish_duration = settings.SETTINGS_ALPHA_VANISH_DURATION
        self._settings_dest_alpha_vanish: int = settings.SETTINGS_DEST_ALPHA_VANISH
        self._control_animation_duration: int = settings.CONTROL_ANIMATION_DURATION

        # control buttons
        self.control_data_path: Path = settings.CONTROL_DATA_PATH
        self.__control_data: list[list[str, int, str]] = self.__load_control_data()

        self.__create_settings_buttons()

    def __create_settings_buttons(self) -> None:  # TODO remove code duplications
        # params: return tuple with buttons and dest pos
        x: int = settings.CONTROL_X
        y, y_offset = settings.CONTROL_Y, settings.CONTROL_Y_OFFSET  # todo ref
        dest_pos_y = y

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

    def scroll_menu(self, event_key: int) -> None:  # todo doc
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

    # def display_settings_menu(self, status: Status) -> None:  # todo doc
    #     for button in self.buttons_list:
    #         button.set_scroll_opacity()
    #         button.control_button.set_scroll_opacity()
    #     self.alpha_vanish(self._settings_alpha_vanish_duration, self.settings_dropdown_start_time, 0,
    #                       self._settings_dest_alpha_vanish, self.settings_fade_surf)
    #
    #     self.dropdown_menu_effect(self.buttons_list, self.settings_dropdown_start_time,
    #                               self._control_animation_duration, self.y_dest_positions)
    #
    #     control_list = [button.control_button for button in self.buttons_list]  # TODO fix this
    #
    #     self.dropdown_menu_effect(control_list, self.settings_dropdown_start_time, self._control_animation_duration,
    #                               self.y_dest_positions)
    #
    #     if status == Status.SET_CONTROL:
    #         for button in self.buttons_list:
    #             if button.control_button.selected:
    #                 button.blinking_effect()
    #                 button.control_button.blinking_effect()
    #
    #             self.display_surface.blit(button.surf, button.rect)
    #             self.display_surface.blit(button.control_button.surf, button.control_button.rect)
    #     else:
    #
    #         for button in self.buttons_list:
    #             button.fade_in_hover()
    #             button.control_button.fade_in_hover()
    #
    #             self.display_surface.blit(button.surf, button.rect)
    #             self.display_surface.blit(button.control_button.surf, button.control_button.rect)
