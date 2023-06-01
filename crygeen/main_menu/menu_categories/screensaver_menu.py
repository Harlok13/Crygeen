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
        # general setup
        self.screen_size: tuple[int, int] = pg.display.get_window_size()

        # bg opacity effect
        self.flag: bool = False
        self.fade_surf: Surface = pg.Surface(self.screen_size)
        self.fade_surf.set_alpha(255)
        self.dropdown_start_time: int = 0
        self.alpha_vanish_duration: int = settings.SCREENSAVER_ALPHA_VANISH_DURATION
        self.start_alpha_vanish_opacity: int = settings.SCREENSAVER_START_ALPHA_VANISH_OPACITY
        self.end_alpha_vanish_opacity: int = settings.SCREENSAVER_END_ALPHA_VANISH_OPACITY
        # text opacity effect
        self.text_alpha_duration: int = settings.SCREENSAVER_TEXT_ALPHA_DURATION
        self.text_alpha: tuple[int, int] = settings.SCREENSAVER_TEXT_ALPHA
        self.text_end_alpha: int = settings.SCREENSAVER_TEXT_END_ALPHA
        self.animation_start_time: int = 0

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

        screensaver_scale_data: list[Surface] = [
            pg.transform.scale(item, self.screen_size) for item in screensaver_data
        ]

        return screensaver_scale_data
