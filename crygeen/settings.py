import os
from typing import Tuple

import pygame as pg
from pydantic import BaseSettings

from crygeen.states import State, Status


# TODO make the coordinates depend on the screen size
# TODO make font size dependent on screen size
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

    SAVE_LOAD_BASE_PATH: str = f'{BASE_PATH}/data'
    CONTROL_DATA_PATH: str = f'{SAVE_LOAD_BASE_PATH}/control'
    NAME_CONTROL_FILE: str = 'control_save.json'

    # TODO use Path instead (Voko)
    MAIN_MENU_LIST_old: list[str] = ['New Game', 'Load game', 'Settings', 'Exit']
    MAIN_MENU_LIST: dict = {
        'New Game': {
            'status': Status.NEW_GAME
        },
        'Load game': {
            'status': Status.LOAD_GAME
        },
        'Settings': {
            'status': Status.SETTINGS
        },
        'Exit': {
            'status': Status.EXIT,
        }
    }
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
    SCREENSAVER_SURF_COLOR: Tuple[int, int, int] = (0, 0, 0)  # black
    SCREENSAVER_ALPHA_VANISH_DURATION: int = 10000

    SOUND_CLICK: str = f'{BASE_PATH}/audio/click.ogg'

    EXIT_LIST: dict = {
        'No':
            {
                'status': Status.MAIN_MENU
            },
        'Yes':
            {
                'action': 'pg.quit(); exit()'
            }
    }
    EXIT_BUTTON_Y: int = 500
    EXIT_BUTTON_X: tuple[int, int] = (SCREEN_WIDTH // 2 - 200, SCREEN_WIDTH // 2 + 200)
    EXIT_BUTTON_POSITION: str = 'center'

    CONTROL_TITLE: str = 'Control Setup'
    CONTROL_ALPHA: int = 228
    CONTROL_SELECT_COLOR: tuple = (255, 0, 0)  # red
    CONTROL_X: int = SCREEN_WIDTH // 2 or 2.5
    CONTROL_Y: int = SCREEN_HEIGHT // 8
    CONTROL_Y_OFFSET: int = 10 + MAIN_MENU_FONT_SIZE
    CONTROL_FONT_SIZE: int = 30
    SETTINGS_ALPHA_VANISH_DURATION: int = 1000

    CONTROL: dict = {
        'left': pg.K_a,
        'right': pg.K_d,
        'up': pg.K_w,
        'down': pg.K_s,
        'pause': pg.K_ESCAPE,
        'interaction': pg.K_e,
        'inventory': pg.K_TAB,
        'spurt': pg.KMOD_SHIFT,
        'action': pg.K_SPACE,
        'slot 1': pg.K_1,
        'slot 2': pg.K_2,
        'slot 3': pg.K_3
    }


settings = Settings()
