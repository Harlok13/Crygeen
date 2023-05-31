import math
import operator
from typing import Callable

import pygame as pg
from pygame import Surface, Rect
from pygame.font import Font

from crygeen.main_menu.buttons import Button, ControlButton
from crygeen.main_menu.states import Status
from crygeen.settings import settings


class MenuAnimation:

    def alpha_vanish(
            self,
            duration: int,
            start_time: int,
            start_alpha: int,
            end_alpha: int,
            fade_surface: Surface,
            canvas: Surface,
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

        fade_surface.fill(color)
        delta: int = pg.time.get_ticks() - start_time
        erp_alpha: float = self._lerp(start_alpha, end_alpha, delta / duration)
        if op(erp_alpha, end_alpha):  # < or >
            fade_surface.set_alpha(erp_alpha)  # type: ignore
        canvas.blit(fade_surface, (0, 0))

    def dropdown_menu_effect(  # todo fix shading
            self,
            buttons_list: list[Button],
            start_time: int,
            animation_duration: int,
            y_dest_positions: list[int],
            shading: bool = False
    ) -> None:
        """
        Play animation, when open main_menu.
        :return: None
        """
        opacity_values = (128, 0) if shading else (0, 128)  # TODO: ref hard code
        if animation_duration > 0:
            delta: int = pg.time.get_ticks() - start_time
            for button in buttons_list:
                if delta < animation_duration:
                    button.rect.y = self._lerp(
                        button.rect.y, y_dest_positions[button.index], delta / animation_duration
                    )
                    button.surf.set_alpha(self._lerp(
                        *opacity_values, delta / animation_duration
                    ))

    @staticmethod
    def _lerp(a: float, b: float, t: float) -> float | int:
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
    def _add_text_effect(obj: Surface) -> None:
        item_alpha: int = int(abs(math.sin(pg.time.get_ticks() / 1000)) * 128 + 128)
        obj.set_alpha(item_alpha)

    def draw_text(
            self, text: str, font: Font, x: int, y: int, font_color: tuple = settings.MAIN_MENU_FONT_COLOR
    ) -> tuple[Surface, Rect]:
        """
        Draw a text on the screen.
        :param text: The text to be displayed.
        :param font: The font used for the text.
        :param x: The x-coordinate of the starting point of text display.
        :param y: The y-coordinate of the starting point of text display.
        :return:
        """
        text_surf: Surface = font.render(text, True, font_color)
        text_rect: Rect = text_surf.get_rect()
        text_rect.center = (x, y)

        return text_surf, text_rect,


class MenuPlayer:
    def __init__(
            self, menu, exit_menu, settings_menu, screensaver_menu
    ):  # type: ('Menu', 'ExitMenu', 'SettingsMenu', 'ScreensaverMenu') -> None

        self.display_surface: Surface = pg.display.get_surface()

        self.menu = menu
        self.exit_menu = exit_menu
        self.settings_menu = settings_menu
        self.screensaver_menu = screensaver_menu

        self.animation: MenuAnimation = MenuAnimation()

        self.status: Status = Status.SCREENSAVER

        # flags setup
        self.play_exit_menu: bool = False
        self.play_main_menu: bool = False
        self.play_settings_menu: bool = False
        self.play_load_game_menu: bool = False
        self.play_new_game_menu: bool = False

    def start_screensaver(self) -> None:
        if not self.screensaver_menu.flag:
            self.screensaver_menu.animation_start_time = pg.time.get_ticks()
            self.screensaver_menu.flag = True
        self.screensaver_menu.frame_idx = (self.screensaver_menu.frame_idx + 1) % self.screensaver_menu.count_frames

        self.display_surface.blit(self.screensaver_menu.bg_data[self.screensaver_menu.frame_idx], (0, 0))

        self.animation.alpha_vanish(self.screensaver_menu.alpha_vanish_duration,
                                    self.screensaver_menu.animation_start_time,
                                    self.screensaver_menu.start_alpha_vanish, 0,
                                    self.screensaver_menu.fade_surf, self.display_surface)

        if self.status == Status.SCREENSAVER:
            draw_text_decorator: Callable = self.screensaver_menu.screensaver_text_effect(
                self.screensaver_menu.start_text_alpha,
                self.screensaver_menu.alpha_text_duration,
                self.screensaver_menu.animation_start_time
            )(self.animation.draw_text)

            self.display_surface.blit(
                *draw_text_decorator(
                    text=self.screensaver_menu.text,
                    font=self.screensaver_menu.font,
                    x=self.screensaver_menu.text_x,
                    y=self.screensaver_menu.text_y,
                ))

    def close_exit_menu(self) -> None:
        if self.status != Status.SCREENSAVER:  # todo any idea?
            self.animation.dropdown_menu_effect(
                self.exit_menu.buttons_list, self.exit_menu.animation_start_time, self.exit_menu.dropdown_duration,
                [1000] * len(self.exit_menu.buttons_list), True
            )
            self.animation.alpha_vanish(
                self.exit_menu.alpha_vanish_duration,
                self.menu.animation_start_time,  # todo fix time
                200,  # todo ref naming and values
                0,
                self.exit_menu.fade_surf,
                self.display_surface
            )
            for button in self.exit_menu.buttons_list:
                self.display_surface.blit(button.surf, button.rect)

    def start_exit_menu(self):
        if self.play_exit_menu:
            self.animation.alpha_vanish(
                self.exit_menu.alpha_vanish_duration,
                self.exit_menu.animation_start_time,
                self.exit_menu.start_alpha_vanish,
                self.exit_menu.end_alpha_vanish,
                self.exit_menu.fade_surf,
                self.display_surface
            )

            self.display_surface.blit(
                *self.animation.draw_text(self.exit_menu.text, self.exit_menu.font, self.exit_menu.text_x,
                                          self.exit_menu.text_y)
            )

            self.animation.dropdown_menu_effect(
                self.exit_menu.buttons_list,
                self.exit_menu.animation_start_time,
                self.exit_menu.dropdown_duration,
                self.exit_menu.button_dest_y,
            )

            for button in self.exit_menu.buttons_list:
                button.fade_in_hover()
                self.display_surface.blit(button.surf, button.rect)
        else:
            self.close_exit_menu()

    def start_menu(self) -> None:
        if self.status != Status.SCREENSAVER:
            if self.play_main_menu:
                self.animation.dropdown_menu_effect(
                    self.menu.buttons_list, self.menu.animation_start_time, self.menu.dropdown_duration,
                    self.menu.y_dest_positions
                )

                for button in self.menu.buttons_list:
                    button.fade_in_hover()
                    self.display_surface.blit(button.surf, button.rect)
            else:
                self.close_menu()

    def close_menu(self) -> None:
        self.animation.dropdown_menu_effect(
            self.menu.buttons_list, self.menu.animation_start_time, self.menu.dropdown_duration,
            [1000] * len(self.menu.buttons_list), True
        )  # TODO ref hard code

        for button in self.menu.buttons_list:
            self.display_surface.blit(button.surf, button.rect)

    def start_settings_menu(self):
        if self.play_settings_menu:
            for button in self.settings_menu.buttons_list:
                button.set_scroll_opacity()
                button.control_button.set_scroll_opacity()

            self.animation.alpha_vanish(self.settings_menu.alpha_vanish_duration,
                                        self.settings_menu.animation_start_time, 0,
                                        self.settings_menu.dest_alpha_vanish,
                                        self.settings_menu.fade_surf, self.display_surface)

            self.animation.dropdown_menu_effect(self.settings_menu.buttons_list,
                                                self.settings_menu.animation_start_time,
                                                self.settings_menu.control_dropdown_duration,
                                                self.settings_menu.y_dest_positions)

            control_buttons_list: list[ControlButton] = [button.control_button for button in
                                                         self.settings_menu.buttons_list]  # TODO fix this

            self.animation.dropdown_menu_effect(control_buttons_list, self.settings_menu.animation_start_time,
                                                self.settings_menu.control_dropdown_duration,
                                                self.settings_menu.y_dest_positions)

            if self.status == Status.SET_CONTROL:
                for button in self.settings_menu.buttons_list:
                    if button.control_button.selected:
                        button.blinking_effect()
                        button.control_button.blinking_effect()

                    self.display_surface.blit(button.surf, button.rect)
                    self.display_surface.blit(button.control_button.surf, button.control_button.rect)
            else:

                for button in self.settings_menu.buttons_list:
                    button.fade_in_hover()
                    button.control_button.fade_in_hover()

                    self.display_surface.blit(button.surf, button.rect)
                    self.display_surface.blit(button.control_button.surf, button.control_button.rect)
        else:
            self.close_settings_menu()

    def close_settings_menu(self) -> None:
        self.animation.dropdown_menu_effect(
            self.settings_menu.buttons_list, self.settings_menu.animation_start_time,
            self.settings_menu.control_dropdown_duration,
            [-100] * len(self.settings_menu.buttons_list), True
        )
        control_buttons_list: list[ControlButton] = [button.control_button for button in
                                                     self.settings_menu.buttons_list]  # TODO fix this

        self.animation.dropdown_menu_effect(control_buttons_list, self.settings_menu.animation_start_time,
                                            self.settings_menu.control_dropdown_duration,
                                            [-100] * len(control_buttons_list), True)

        self.animation.alpha_vanish(self.settings_menu.alpha_vanish_duration,
                                    self.settings_menu.animation_start_time, 128,  # todo reloc to settings
                                    0,
                                    self.settings_menu.fade_surf, self.display_surface)

        for button in self.settings_menu.buttons_list:
            self.display_surface.blit(button.surf, button.rect)
            self.display_surface.blit(button.control_button.surf, button.control_button.rect)

    def update(self) -> None:
        self.start_screensaver()
        self.start_menu()
        self.start_settings_menu()
        self.start_exit_menu()

        # if self.play_main_menu:
        #     self.start_menu()
        # else:
        #     self.close_menu()
        #
        # if self.play_exit_menu:
        #     self.start_exit_menu()
        # else:
        #     self.close_exit_menu()
        #
        # if self.play_settings_menu:
        #     self.start_settings_menu()
        # else:
        #     self.close_settings_menu()
        #
        # if self.play_load_game_menu:
        #     self.start_load_game_menu()
        # else:
        #     self.close_load_game_menu()
        #
        # if self.play_new_game_menu:
        #     self.start_new_game_menu()
        # else:
        #     self.close_new_game_menu()
        #
        #
        # self.start_screensaver()
        # if self.status != Status.SCREENSAVER:
        #     self.start_menu()
        # if self.status == Status.EXIT:
        #     self.start_exit_menu()
        # elif self.status == Status.SETTINGS or self.status == Status.SET_CONTROL:
        #     self.start_settings_menu()


class MenuAction:
    def __init__(self):
        pass
