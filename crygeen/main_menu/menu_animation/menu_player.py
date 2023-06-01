import math
import operator
from collections import namedtuple
from functools import wraps
from typing import Callable

import pygame as pg
from pygame import Surface, Rect
from pygame.font import Font

from crygeen.main_menu.buttons import Button, ControlButton
from crygeen.main_menu.menu_animation.animation_properties import AnimationProperty
from crygeen.main_menu.menu_animation.menu_animation import MenuAnimation
from crygeen.main_menu.states import Status
from crygeen.settings import settings
from crygeen.utils.support import deprecated


class MenuPlayer:
    def __init__(
            self, menu, exit_menu, settings_menu, screensaver_menu

    ):  # type: ('Menu', 'ExitMenu', 'SettingsMenu', 'ScreensaverMenu') -> None

        # general setup
        self.display_surface: Surface = pg.display.get_surface()
        self.status: Status = Status.SCREENSAVER

        # init categories
        self.menu = menu
        self.exit_menu = exit_menu
        self.settings_menu = settings_menu
        self.screensaver_menu = screensaver_menu

        # init support class
        self.animation: MenuAnimation = MenuAnimation()

        # menu active flags setup
        self.active_exit_menu: bool = False
        self.active_main_menu: bool = False
        self.active_settings_menu: bool = False
        self.active_load_game_menu: bool = False
        self.active_new_game_menu: bool = False

        # init properties
        self.properties = AnimationProperty(
            self.menu, self.settings_menu, self.screensaver_menu, self.exit_menu
        ).properties

    def start_screensaver(self) -> None:
        # get animation_start_time for screensaver
        if not self.screensaver_menu.flag:
            self.screensaver_menu.animation_start_time = pg.time.get_ticks()
            self.screensaver_menu.flag = True

        # render main bg
        self.screensaver_menu.frame_idx = (self.screensaver_menu.frame_idx + 1) % self.screensaver_menu.count_frames
        self.display_surface.blit(self.screensaver_menu.bg_data[self.screensaver_menu.frame_idx], (0, 0))

        # render effect
        self.animation.alpha_vanish(
            *self.properties['screensaver_start--alpha_vanish'], self.screensaver_menu.animation_start_time
        )

        # show start text
        if self.status == Status.SCREENSAVER:
            draw_text_decorator: Callable = self.animation.screensaver_text_effect(
                *self.properties['screensaver_start--text_effect'], self.screensaver_menu.animation_start_time
            )(self.animation.draw_text)  # call decorator

            # render and animate text
            self.display_surface.blit(
                *draw_text_decorator(*self.properties['screensaver_start--text_decoration'])
            )

    def start_menu(self) -> None:
        if self.status != Status.SCREENSAVER:

            if self.active_main_menu:

                # render start dropdown
                self.animation.dropdown_menu_effect(
                    *self.properties.get('menu_start--dropdown'), self.menu.animation_start_time
                )

                # render buttons and fade effect
                for button in self.menu.buttons_list:
                    button.fade_in_hover()
                    self.display_surface.blit(button.surf, button.rect)

            else:

                self.__close_menu()

    def __close_menu(self) -> None:
        # render close dropdown
        self.animation.dropdown_menu_effect(
            *self.properties.get('menu_close--dropdown'), self.menu.animation_start_time
        )

        # render buttons
        for button in self.menu.buttons_list:
            self.display_surface.blit(button.surf, button.rect)

    def start_settings_menu(self):
        if self.active_settings_menu:

            # set scroll effect
            for button in self.settings_menu.buttons_list:
                button.set_scroll_opacity()
                button.control_button.set_scroll_opacity()

            # render effects
            self.animation.alpha_vanish(
                *self.properties['settings_start--alpha_vanish'], self.settings_menu.animation_start_time
            )
            self.animation.dropdown_menu_effect(
                *self.properties['settings_start--button_dropdown'], self.settings_menu.animation_start_time
            )
            self.animation.dropdown_menu_effect(
                *self.properties['settings_start--control_button_dropdown'], self.settings_menu.animation_start_time,
            )

            # render buttons
            if self.status == Status.SET_CONTROL:

                # render active button
                for button in self.settings_menu.buttons_list:
                    if button.control_button.selected:
                        button.blinking_effect()
                        button.control_button.blinking_effect()

                    self.display_surface.blit(button.surf, button.rect)
                    self.display_surface.blit(button.control_button.surf, button.control_button.rect)

            else:

                # render buttons and fade effect
                for button in self.settings_menu.buttons_list:
                    button.fade_in_hover()
                    button.control_button.fade_in_hover()

                    self.display_surface.blit(button.surf, button.rect)
                    self.display_surface.blit(button.control_button.surf, button.control_button.rect)

        else:

            self.__close_settings_menu()

    def __close_settings_menu(self) -> None:
        # render effects
        self.animation.dropdown_menu_effect(
            *self.properties['settings_close--button_dropdown'], self.settings_menu.animation_start_time,
        )
        self.animation.dropdown_menu_effect(
            *self.properties['settings_close--control_button_dropdown'], self.settings_menu.animation_start_time,
        )
        self.animation.alpha_vanish(
            *self.properties['settings_close--alpha_vanish'], self.settings_menu.animation_start_time,
        )

        # render buttons
        for button in self.settings_menu.buttons_list:
            self.display_surface.blit(button.surf, button.rect)
            self.display_surface.blit(button.control_button.surf, button.control_button.rect)

    def start_exit_menu(self):
        if self.active_exit_menu:

            # render effects
            self.animation.alpha_vanish(
                *self.properties['exit_start--alpha_vanish'], self.exit_menu.animation_start_time,
            )
            self.animation.dropdown_menu_effect(
                *self.properties['exit_start--dropdown'], self.exit_menu.animation_start_time,
            )

            # render and animate text
            draw_text_decorator: Callable = self.animation.screensaver_text_effect(
                *self.properties['exit_start--text_effect'], self.exit_menu.animation_start_time
            )(self.animation.draw_text)  # call decorator

            self.display_surface.blit(
                *draw_text_decorator(*self.properties['exit_start--text_decoration'])
            )

            # render buttons
            for button in self.exit_menu.buttons_list:
                button.fade_in_hover()
                self.display_surface.blit(button.surf, button.rect)

        else:

            self.__close_exit_menu()

    def __close_exit_menu(self) -> None:
        # render effects
        self.animation.dropdown_menu_effect(
            *self.properties['exit_close--dropdown'], self.exit_menu.animation_start_time,
        )
        self.animation.alpha_vanish(  # todo dynamic variable
            self.exit_menu.alpha_vanish_duration,
            self.exit_menu.end_alpha_vanish_opacity if self.screensaver_menu.fade_surf.get_alpha() == 0 else 1,
            self.exit_menu.start_alpha_vanish_opacity,
            self.exit_menu.fade_surf,
            self.display_surface,
            # *self.properties['exit_close--alpha_vanish'],
            self.menu.animation_start_time,
        )

        # render buttons
        for button in self.exit_menu.buttons_list:
            self.display_surface.blit(button.surf, button.rect)

    def update(self) -> None:
        self.start_screensaver()
        if self.status != Status.SCREENSAVER:
            self.start_menu()
            self.start_settings_menu()
            self.start_exit_menu()
