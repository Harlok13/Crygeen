from enum import Enum


class State(Enum):
    MAIN_MENU: str = 'MAIN_MENU'
    GAME: str = 'GAME'


class Status(Enum):
    SCREENSAVER: str = 'SCREENSAVER'
    MAIN_MENU: str = 'MAIN_MENU'
    EXIT: str = 'EXIT'
    SETTINGS: str = 'SETTINGS'
    NEW_GAME: str = 'NEW_GAME'
    LOAD_GAME: str = 'LOAD_GAME'
    SET_CONTROL: str = 'SET_CONTROL'
