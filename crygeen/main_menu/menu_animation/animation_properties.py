from typing import Any

import pygame as pg
from pygame import Surface


class AnimationProperty:
    def __init__(self, menu, settings_menu, screensaver_menu, exit_menu) -> None:
        # general setup
        self.display_surface: Surface = pg.display.get_surface()

        # init categories
        self.menu = menu
        self.settings_menu = settings_menu
        self.screensaver_menu = screensaver_menu
        self.exit_menu = exit_menu

        # init properties
        self.properties: dict[str, Any] = {

            # screensaver animation
            'screensaver_start--alpha_vanish': (
                self.screensaver_menu.alpha_vanish_duration,
                self.screensaver_menu.start_alpha_vanish_opacity,
                self.screensaver_menu.end_alpha_vanish_opacity,
                self.screensaver_menu.fade_surf,
                self.display_surface
            ),
            'screensaver_start--text_effect': (
                self.screensaver_menu.text_alpha,
                self.screensaver_menu.text_alpha_duration,
                self.screensaver_menu.text_end_alpha,
                True
            ),
            'screensaver_start--text_decoration': (
                self.screensaver_menu.text,
                self.screensaver_menu.font,
                self.screensaver_menu.text_x,
                self.screensaver_menu.text_y,
            ),

            # menu animation
            'menu_start--dropdown': (
                self.menu.buttons_list,
                self.menu.dropdown_duration,
                self.menu.y_dest_positions,
                False
            ),

            'menu_close--dropdown': (
                self.menu.buttons_list,
                self.menu.dropdown_duration,
                self.menu.menu_close_y,
                True
            ),

            # settings animation
            'settings_start--alpha_vanish': (
                self.settings_menu.alpha_vanish_duration,
                self.settings_menu.start_alpha_vanish_opacity,
                self.settings_menu.end_alpha_vanish_opacity,
                self.settings_menu.fade_surf,
                self.display_surface
            ),
            'settings_start--button_dropdown': (
                self.settings_menu.buttons_list,
                self.settings_menu.control_dropdown_duration,
                self.settings_menu.y_dest_positions,
                False
            ),
            'settings_start--control_button_dropdown': (
                self.settings_menu.control_buttons_list,
                self.settings_menu.control_dropdown_duration,
                self.settings_menu.y_dest_positions,
                False
            ),

            'settings_close--button_dropdown': (
                self.settings_menu.buttons_list,
                self.settings_menu.control_dropdown_duration,
                self.settings_menu.control_close_y,
                True
            ),
            'settings_close--control_button_dropdown': (
                self.settings_menu.control_buttons_list,
                self.settings_menu.control_dropdown_duration,
                self.settings_menu.control_close_y,
                True
            ),
            'settings_close--alpha_vanish': (
                self.settings_menu.alpha_vanish_duration,
                self.settings_menu.end_alpha_vanish_opacity,
                self.settings_menu.start_alpha_vanish_opacity,
                self.settings_menu.fade_surf,
                self.display_surface
            ),

            # exit animation
            'exit_start--alpha_vanish': (
                self.exit_menu.alpha_vanish_duration,
                self.exit_menu.start_alpha_vanish_opacity,
                self.exit_menu.end_alpha_vanish_opacity,
                self.exit_menu.fade_surf,
                self.display_surface
            ),
            'exit_start--dropdown': (
                self.exit_menu.buttons_list,
                self.exit_menu.dropdown_duration,
                self.exit_menu.button_dest_y,
                False
            ),
            'exit_start--text_effect': (
                self.exit_menu.text_alpha,
                self.exit_menu.text_alpha_duration,
                self.exit_menu.text_end_alpha,
                False
            ),
            'exit_start--text_decoration': (
                self.exit_menu.text,
                self.exit_menu.font,
                self.exit_menu.text_x,
                self.exit_menu.text_y
            ),

            'exit_close--alpha_vanish': (  # not used
                self.exit_menu.alpha_vanish_duration,
                self.exit_menu.start_alpha_vanish_opacity,
                0,
                self.exit_menu.fade_surf,
                self.display_surface,
            ),
            'exit_close--dropdown': (
                self.exit_menu.buttons_list,
                self.exit_menu.dropdown_duration,
                self.exit_menu.exit_close_y,
                True
            )
        }
