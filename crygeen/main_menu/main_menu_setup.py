import random
from typing import Optional, Callable

import pygame as pg
from pygame.mixer import Sound
from pygame import QUIT, KEYDOWN, KEYUP, Surface, MOUSEBUTTONDOWN, MOUSEWHEEL, Rect

from crygeen import audio
from crygeen.main_menu.menu_animation_player import MenuPlayer
from crygeen.main_menu.menu_categories.exit_menu import ExitMenu
from crygeen.main_menu.menu_categories.menu import Menu
from crygeen.main_menu.particles import ParticlePlayer
from crygeen.main_menu.menu_categories.screensaver_menu import ScreensaverMenu
from crygeen.main_menu.menu_categories.settings_menu import SettingsMenu
from crygeen.main_menu.saver import SaveLoadManager


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
        self.menu_player: MenuPlayer = MenuPlayer(
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
        self.__simple_toggle_music()
        self.menu_player.update()
        self.cursor.update()
