import math
from functools import wraps
from pathlib import Path
from typing import Callable

import pygame as pg
from pygame import Surface, Rect
from pygame.font import Font

from crygeen.main_menu.menu_categories.menu import Menu
from crygeen.main_menu.states import Status
from crygeen.settings import settings
from crygeen.utils.support import import_folder_img


class ScreensaverMenu(Menu):
    def __init__(self):
        super().__init__()
        self.screensaver_active: bool = True

        # bg opacity effect
        self._screensaver_flag: bool = False
        self.screensaver_fade_surf: Surface = pg.Surface(self.screen_size)
        self.screensaver_fade_surf.set_alpha(255)
        self._screensaver_dropdown_start_time: int = 0
        self._screensaver_alpha_vanish_duration: int = settings.SCREENSAVER_ALPHA_VANISH_DURATION
        self._screensaver_start_alpha_vanish: int = settings.SCREENSAVER_START_ALPHA_VANISH
        # text opacity effect
        self._screensaver_alpha_text_duration: int = settings.SCREENSAVER_ALPHA_TEXT_DURATION
        self._screensaver_start_text_alpha: tuple[int, int] = settings.SCREENSAVER_START_TEXT_ALPHA

        # screensaver bg
        self._screensaver_path: Path = settings.SCREENSAVER_PATH
        self._screensaver_data: list[Surface] = self.__load_screensaver_data()
        self._count_frames: int = len(self._screensaver_data)
        self._screensaver_frame_idx: int = 0

        # screensaver text
        self._screensaver_text: str = settings.SCREENSAVER_TEXT
        self._screensaver_font_size: int = settings.SCREENSAVER_FONT_SIZE
        self._screensaver_font: Font = pg.font.Font(settings.SCREENSAVER_FONT, self._screensaver_font_size)
        self._screensaver_text_x: int = self.screen_size[0] // 2 or settings.SCREENSAVER_TEXT_X
        self._screensaver_text_y: int = settings.SCREENSAVER_TEXT_Y

    def __load_screensaver_data(self) -> list[Surface]:
        """
        Create list of screensaver surfaces and optimize size according to screen size.
        :return: List of surfaces needed for animation.
        """
        screensaver_data: list[Surface] = import_folder_img(self._screensaver_path)

        screensaver_scale_data: list[Surface] = [pg.transform.scale(item, (1280, 800)) for item in
                                                 screensaver_data]  # TODO ref hard code

        return screensaver_scale_data

    @staticmethod
    def _screensaver_text_effect(alpha_values: tuple[int, int], emergence_duration: int, start_time: int) -> Callable:
        def outer_wrapper(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> tuple[Surface, Rect]:

                text_surf, text_rect = func(*args, **kwargs)

                delta: int = pg.time.get_ticks() - start_time
                start_alpha, end_alpha = alpha_values
                dt: float = delta / emergence_duration
                alpha_offset: float | int = start_alpha + (end_alpha - start_alpha) * dt

                if alpha_offset <= 200:
                    text_surf.set_alpha(alpha_offset)
                else:
                    wave_alpha: int = int(abs(math.sin(pg.time.get_ticks() / 1000)) * 128 + 128)
                    text_surf.set_alpha(wave_alpha)

                return text_surf, text_rect

            return wrapper

        return outer_wrapper

    def start_screensaver(self, status: Status) -> None:
        """
        Draws a splash screen when the application starts.
        :return: None
        """
        if not self._screensaver_flag:
            self._screensaver_dropdown_start_time: int = pg.time.get_ticks()
            self._screensaver_flag: bool = True
        self._screensaver_frame_idx: int = (self._screensaver_frame_idx + 1) % self._count_frames

        self.display_surface.blit(self._screensaver_data[self._screensaver_frame_idx], (0, 0))

        self.alpha_vanish(self._screensaver_alpha_vanish_duration, self._screensaver_dropdown_start_time,
                          self._screensaver_start_alpha_vanish, 0, self.screensaver_fade_surf)

        if status == Status.SCREENSAVER:
            draw_text_decorator: Callable = self._screensaver_text_effect(
                self._screensaver_start_text_alpha,
                self._screensaver_alpha_text_duration,
                self._screensaver_dropdown_start_time
            )(self.draw_text)

            self.display_surface.blit(
                *draw_text_decorator(
                    text=self._screensaver_text,
                    font=self._screensaver_font,
                    x=self._screensaver_text_x,
                    y=self._screensaver_text_y,
                ))
