from pathlib import Path

import pygame as pg

from crygeen.main_menu.buttons import LinkedList, Button, ControlButton
from crygeen.main_menu.controls import Control, Key
from crygeen.main_menu.menu_categories.menu import Menu
from crygeen.main_menu.states import Status
from crygeen.settings import settings


class SettingsMenu(Menu):
    def __init__(self):
        super().__init__()
        self.linked_list: LinkedList = LinkedList()
        self.control_list: Control = settings.CONTROL
        self.control_buttons_list: list = []
        self._control_y_dest_positions: list = []
        self._control_buttons_position: str = settings.CONTROL_BUTTONS_POSITION
        self._control_bottom_boundary: int = settings.CONTROL_BOTTOM_BOUNDARY
        self._control_top_boundary: int = settings.CONTROL_TOP_BOUNDARY
        self._control_scroll_offset: int = settings.CONTROL_SCROLL_OFFSET

        # control buttons
        self.control_data_path: Path = settings.CONTROL_DATA_PATH
        self.__control_data: list[list[str, int, str]] = self.__load_control_data()

        self.__create_settings_buttons()

        # settings effects
        self.settings_fade_surf = pg.Surface(self._screen_size)
        self.settings_fade_surf.set_alpha(0)
        self.settings_dropdown_start_time: int = 0
        self._settings_alpha_vanish_duration = settings.SETTINGS_ALPHA_VANISH_DURATION
        self._settings_dest_alpha_vanish: int = settings.SETTINGS_DEST_ALPHA_VANISH
        self._control_animation_duration: int = settings.CONTROL_ANIMATION_DURATION

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
                "font_name": self.main_menu_font_name,
                "font_size": settings.CONTROL_FONT_SIZE,
                "font_color": self.main_menu_font_color,
                "position": self._control_buttons_position,
                "opacity_offset": self.button_opacity_offset,
                "alpha": self.alpha,
                "index": index,
                "properties": "",
            }
            button: Button = Button(
                **button_kwargs,
                control_button=ControlButton(title=f"{self.__control_data[index][2]}",
                                             x=1000,  # todo ref
                                             y=y,
                                             font_name=self.main_menu_font_name,
                                             font_size=settings.CONTROL_FONT_SIZE,
                                             font_color=self.main_menu_font_color,
                                             position='topright',
                                             opacity_offset=self.button_opacity_offset,
                                             alpha=self.alpha,
                                             index=index,
                                             properties="",
                                             constant=self.__control_data[index][1],  # type: ignore
                                             key=self.__control_data[index][2],

                                             )
            )
            self.linked_list.append(button)
            self._control_y_dest_positions.append(dest_pos_y)
            self.control_buttons_list.append(button)

    def scroll_menu_old(self, event_key: int) -> None:  # todo doc
        match event_key:
            case pg.SYSTEM_CURSOR_WAITARROW:
                if self.linked_list.head.button.rect.y <= self._control_bottom_boundary:
                    self.linked_list.set_y_offset(self._control_scroll_offset)

            case pg.SYSTEM_CURSOR_SIZENWSE:
                if self.linked_list.tail.button.rect.y >= self._control_top_boundary:
                    self.linked_list.set_y_offset(-self._control_scroll_offset)

    def scroll_menu(self, event_key: int) -> None:  # todo doc
        if event_key == 4:
            if self.linked_list.head.button.rect.y <= self._control_bottom_boundary:
                self.linked_list.set_y_offset(self._control_scroll_offset)

        elif event_key == 5:
            if self.linked_list.tail.button.rect.y >= self._control_top_boundary:
                self.linked_list.set_y_offset(-self._control_scroll_offset)

    def __load_control_data(self) -> list[list[str, int, str]]:
        try:
            return self.save_load_manager.load_save(self.control_data_path)
        except FileNotFoundError:
            self.save_load_manager.write_save(self.control_list, self.control_data_path)
            return self.save_load_manager.load_save(self.control_data_path)

    def display_settings_menu(self, status: Status) -> None:  # todo doc
        for button in self.control_buttons_list:
            button.set_scroll_opacity()
            button.control_button.set_scroll_opacity()
        self._alpha_vanish(self._settings_alpha_vanish_duration, self.settings_dropdown_start_time, 0,
                           self._settings_dest_alpha_vanish, self.settings_fade_surf)

        self._dropdown_menu_effect(self.control_buttons_list, self.settings_dropdown_start_time,
                                   self._control_animation_duration, self._control_y_dest_positions)

        control_list = [button.control_button for button in self.control_buttons_list]  # TODO fix this

        self._dropdown_menu_effect(control_list, self.settings_dropdown_start_time, self._control_animation_duration,
                                   self._control_y_dest_positions)

        if status == Status.SET_CONTROL:
            for button in self.control_buttons_list:
                if button.control_button.selected:
                    button.blinking_effect()
                    button.control_button.blinking_effect()

                self._display_surface.blit(button.surf, button.rect)
                self._display_surface.blit(button.control_button.surf, button.control_button.rect)
        else:

            for button in self.control_buttons_list:
                button.fade_in_hover()
                button.control_button.fade_in_hover()

                self._display_surface.blit(button.surf, button.rect)
                self._display_surface.blit(button.control_button.surf, button.control_button.rect)