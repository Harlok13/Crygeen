import random
from typing import Optional

import pygame as pg
from pygame.mixer import Sound
from pygame import QUIT, KEYDOWN, KEYUP, Surface, MOUSEBUTTONDOWN, MOUSEWHEEL

from crygeen import audio
from crygeen.main_menu.menu_categories.exit_menu import ExitMenu
from crygeen.main_menu.menu_categories.menu import Menu
from crygeen.main_menu.particles import ParticlePlayer
from crygeen.main_menu.menu_categories.screensaver_menu import ScreensaverMenu
from crygeen.main_menu.menu_categories.settings_menu import SettingsMenu
from crygeen.main_menu.states import Status


class MainMenuSetup:
    def __init__(self):
        self.status: Status = Status.SCREENSAVER

        self.__main_sound: Sound = pg.mixer.Sound(random.choice(audio.MAIN_MENU_SOUND))
        self.__main_sound.set_volume(audio.MAIN_MENU_VOLUME)
        self.toggle_music_flag: bool = True

        # initialize main_menu
        self.menu: Menu = Menu()
        self.exit_menu: ExitMenu = ExitMenu()
        self.settings_menu: SettingsMenu = SettingsMenu()
        self.screensaver_menu: ScreensaverMenu = ScreensaverMenu()


        self.particle_player = ParticlePlayer()

        self.fps: Optional[int] = None

        pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEWHEEL])

    def __simple_toggle_music(self) -> None:
        if self.toggle_music_flag:
            self.__main_sound.play(loops=audio.MAIN_MENU_LOOPS)
            self.toggle_music_flag: bool = False

    def run_menu(self, status: Status) -> None:
        self.screensaver_menu.start_screensaver(status)
        # self.__simple_toggle_music()
        if status != Status.SCREENSAVER:
            self.menu.display_menu(status, self.exit_menu, self.settings_menu)
        if status == Status.EXIT:
            self.exit_menu.display_exit_menu()
        elif status == Status.SETTINGS or self.status == Status.SET_CONTROL:
            self.settings_menu.display_settings_menu(status)
