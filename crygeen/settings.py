import os
from typing import Tuple

import pygame as pg
from pydantic import BaseSettings


class Settings(BaseSettings):
    SCREEN_WIDTH: int = 1280
    SCREEN_HEIGHT: int = 760
    FLAGS: int = pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
    BIT_PER_PIXEL: int = 32
    BACKGROUND_COLOR: Tuple[int, int, int] = (0, 0, 0)  # black
    STD_BUTTON_COLOR: Tuple[int, int, int] = (255, 255, 255)  # white
    GAME_TITLE: str = "Menu"
    GAME_ICO = ''
    FPS: int = 40
    BASE_PATH: str = os.getcwd()

    # TODO use Path instead (Voko)
    MAIN_MENU_LIST: list[str] = ['New Game', 'Load game', 'Settings', 'Exit']
    MAIN_MENU_FONT: str = f'{BASE_PATH}/assets/graphics/font/AlumniSansInlineOne-italic.ttf'
    MAIN_MENU_POSITION: str = 'topleft'
    MAIN_MENU_X: int = 150
    MAIN_MENU_Y: int = 100
    MAIN_MENU_Y_OFFSET: int = 100
    MAIN_MENU_OPACITY_OFFSET: int = 10  # fade-in hover if button is selected
    MAIN_MENU_ALPHA: int = 128
    MAIN_MENU_FONT_SIZE: int = 50
    MAIN_MENU_FONT_COLOR: Tuple[int, int, int] = (255, 255, 255)  # white

    SCREENSAVER_PATH: str = f'{BASE_PATH}/assets/graphics/screensaver'
    # SCREENSAVER_PATH: str = f'{BASE_PATH}/assets/graphics/main'  # test mode
    SCREENSAVER_ALPHA_OFFSET: float = .5
    SCREENSAVER_FONT: str = f'{BASE_PATH}/assets/graphics/font/AlumniSansInlineOne-italic.ttf'
    SCREENSAVER_FONT_SIZE: int = 45
    SCREENSAVER_FONT_COLOR: Tuple[int, int, int] = (255, 255, 255)  # white
    SCREENSAVER_ALPHA_COLOR: Tuple[int, int, int] = (0, 0, 0)  # black

    SOUND_CLICK: str = f'{BASE_PATH}/audio/click.ogg'


settings = Settings()
