import math
import operator
import random
from typing import Optional, Callable

import pygame as pg
from pygame.font import Font
from pygame.mixer import Sound
from pygame import QUIT, KEYDOWN, KEYUP, Surface, MOUSEBUTTONDOWN, MOUSEWHEEL, Rect

from crygeen import audio
from crygeen.main_menu.buttons import Button
from crygeen.main_menu.menu_categories.exit_menu import ExitMenu
from crygeen.main_menu.menu_categories.menu import Menu
from crygeen.main_menu.particles import ParticlePlayer
from crygeen.main_menu.menu_categories.screensaver_menu import ScreensaverMenu
from crygeen.main_menu.menu_categories.settings_menu import SettingsMenu
from crygeen.main_menu.saver import SaveLoadManager
from crygeen.main_menu.states import Status
from crygeen.settings import settings


class MainMenuSetup:
    def __init__(self):
        self.__main_sound: Sound = pg.mixer.Sound(random.choice(audio.MAIN_MENU_SOUND))
        self.__main_sound.set_volume(audio.MAIN_MENU_VOLUME)
        self.toggle_music_flag: bool = True
        self.save_load_manager: SaveLoadManager = SaveLoadManager()

        self.menu: Menu = Menu()
        self.exit_menu: ExitMenu = ExitMenu()
        self.settings_menu: SettingsMenu = SettingsMenu(self.save_load_manager)
        self.screensaver_menu: ScreensaverMenu = ScreensaverMenu()
        self.animation_player: MenuAnimationPlayer = MenuAnimationPlayer(
            self.menu, self.exit_menu, self.settings_menu, self.screensaver_menu
        )

        self.particle_player = ParticlePlayer()

        self.fps: Optional[int] = None

        pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEWHEEL])

    def __simple_toggle_music(self) -> None:
        if self.toggle_music_flag:
            self.__main_sound.play(loops=audio.MAIN_MENU_LOOPS)
            self.toggle_music_flag: bool = False

    def run_menu(self) -> None:
        self.animation_player.update()


class AnimationSupport:

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

    def dropdown_menu_effect(
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


class MenuAnimationPlayer:
    def __init__(self, menu, exit_menu, settings_menu, screensaver_menu) -> None:
        self.display_surface: Surface = pg.display.get_surface()

        self.menu: Menu = menu
        self.exit_menu: ExitMenu = exit_menu
        self.settings_menu: SettingsMenu = settings_menu
        self.screensaver_menu: ScreensaverMenu = screensaver_menu

        self.animation: AnimationSupport = AnimationSupport()

        self.status: Status = Status.SCREENSAVER

    def start_screensaver(self) -> None:
        if not self.screensaver_menu.flag:
            self.screensaver_menu.dropdown_start_time = pg.time.get_ticks()
            self.screensaver_menu.flag = True
        self.screensaver_menu.frame_idx = (self.screensaver_menu.frame_idx + 1) % self.screensaver_menu.count_frames

        self.display_surface.blit(self.screensaver_menu.bg_data[self.screensaver_menu.frame_idx], (0, 0))

        self.animation.alpha_vanish(self.screensaver_menu.alpha_vanish_duration,
                                    self.screensaver_menu.dropdown_start_time,
                                    self.screensaver_menu.start_alpha_vanish, 0,
                                    self.screensaver_menu.fade_surf, self.display_surface)

        if self.status == Status.SCREENSAVER:
            draw_text_decorator: Callable = self.screensaver_menu.screensaver_text_effect(
                self.screensaver_menu.start_text_alpha,
                self.screensaver_menu.alpha_text_duration,
                self.screensaver_menu.dropdown_start_time
            )(self.animation.draw_text)

            self.display_surface.blit(
                *draw_text_decorator(
                    text=self.screensaver_menu.text,
                    font=self.screensaver_menu.font,
                    x=self.screensaver_menu.text_x,
                    y=self.screensaver_menu.text_y,
                ))

    def start_menu(self) -> None:
        if self.status == Status.MAIN_MENU:
            self.animation.dropdown_menu_effect(
                self.menu.buttons_list, self.menu.dropdown_start_time, self.menu.dropdown_animation_time,
                self.menu.y_dest_positions
            )

            self.animation.dropdown_menu_effect(
                self.exit_menu.buttons_list, self.exit_menu.dropdown_start_time, self.exit_menu.dropdown_duration,
                [1000] * len(self.exit_menu.buttons_list), True
            )
            for button in self.exit_menu.buttons_list:
                self.display_surface.blit(button.surf, button.rect)

        if self.status != Status.MAIN_MENU:
            self.animation.dropdown_menu_effect(
                self.menu.buttons_list, self.menu.dropdown_start_time, self.menu.dropdown_animation_time,
                [1000] * len(self.menu.buttons_list), True
            )  # TODO ref hard code

        for button in self.menu.buttons_list:
            button.fade_in_hover()

            self.display_surface.blit(button.surf, button.rect)

    def start_exit_menu(self):
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

    def start_settings_menu(self):
        for button in self.settings_menu.buttons_list:
            button.set_scroll_opacity()
            button.control_button.set_scroll_opacity()
        self.animation.alpha_vanish(self.settings_menu.alpha_vanish_duration,
                                    self.settings_menu.dropdown_start_time, 0,
                                    self.settings_menu.dest_alpha_vanish,
                                    self.settings_menu.fade_surf, self.display_surface)

        self.animation.dropdown_menu_effect(self.settings_menu.buttons_list,
                                            self.settings_menu.dropdown_start_time,
                                            self.settings_menu.control_animation_duration,
                                            self.settings_menu.y_dest_positions)

        control_list = [button.control_button for button in self.settings_menu.buttons_list]  # TODO fix this

        self.animation.dropdown_menu_effect(control_list, self.settings_menu.dropdown_start_time,
                                            self.settings_menu.control_animation_duration,
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

    def update(self) -> None:
        self.start_screensaver()
        if self.status != Status.SCREENSAVER:
            self.start_menu()
        if self.status == Status.EXIT:
            self.start_exit_menu()
        elif self.status == Status.SETTINGS or self.status == Status.SET_CONTROL:
            self.start_settings_menu()
