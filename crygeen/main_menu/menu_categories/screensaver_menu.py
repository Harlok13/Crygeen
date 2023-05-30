import math
from functools import wraps
from pathlib import Path
from typing import Callable

import pygame as pg
from pygame import Surface, Rect
from pygame.font import Font

from crygeen.settings import settings
from crygeen.utils.support import import_folder_img


class ScreensaverMenu:
    def __init__(self):
        self.screen_size: tuple[int, int] = pg.display.get_window_size()
        # bg opacity effect
        self.flag: bool = False
        self.fade_surf: Surface = pg.Surface(self.screen_size)
        self.fade_surf.set_alpha(255)
        self.dropdown_start_time: int = 0
        self.alpha_vanish_duration: int = settings.SCREENSAVER_ALPHA_VANISH_DURATION
        self.start_alpha_vanish: int = settings.SCREENSAVER_START_ALPHA_VANISH
        # text opacity effect
        self.alpha_text_duration: int = settings.SCREENSAVER_ALPHA_TEXT_DURATION
        self.start_text_alpha: tuple[int, int] = settings.SCREENSAVER_START_TEXT_ALPHA

        # screensaver bg
        self.bg_path: Path = settings.SCREENSAVER_PATH
        self.bg_data: list[Surface] = self.__load_screensaver_data()
        self.count_frames: int = len(self.bg_data)
        self.frame_idx: int = 0

        # screensaver text
        self.text: str = settings.SCREENSAVER_TEXT
        self.font_size: int = settings.SCREENSAVER_FONT_SIZE
        self.font: Font = pg.font.Font(settings.SCREENSAVER_FONT, self.font_size)
        self.text_x: int = self.screen_size[0] // 2 or settings.SCREENSAVER_TEXT_X
        self.text_y: int = settings.SCREENSAVER_TEXT_Y

    def __load_screensaver_data(self) -> list[Surface]:
        """
        Create list of screensaver surfaces and optimize size according to screen size.
        :return: List of surfaces needed for animation.
        """
        screensaver_data: list[Surface] = import_folder_img(self.bg_path)

        screensaver_scale_data: list[Surface] = [pg.transform.scale(item, (1280, 800)) for item in
                                                 screensaver_data]  # TODO ref hard code

        return screensaver_scale_data

    @staticmethod
    def screensaver_text_effect(alpha_values: tuple[int, int], emergence_duration: int, start_time: int) -> Callable:
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

