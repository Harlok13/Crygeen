import random
import time
from typing import Optional

import pygame as pg
from pygame import QUIT, KEYDOWN, KEYUP, Surface, MOUSEBUTTONDOWN, MOUSEWHEEL
from pygame.event import Event
from pygame.mixer import Sound
from pygame.time import Clock

from crygeen import audio
from crygeen.main_menu.buttons import ControlButton, Button
from crygeen.game_process.game_settings import gSettings
from crygeen.game_process.level import Level
from crygeen.game_process.spritesheet import SpriteSheet
from crygeen.main_menu.menu_categories.exit_menu import ExitMenu
from crygeen.main_menu.menu_categories.menu import Menu
from crygeen.main_menu.particles import ParticlePlayer
from crygeen.main_menu.menu_categories.screensaver_menu import ScreensaverMenu
from crygeen.main_menu.menu_categories.settings_menu import SettingsMenu

from crygeen.settings import settings
from crygeen.main_menu.states import Status, State


class EventHandler:
    def __init__(self) -> None:
        self.game: Optional[Game] = None

        self.select_button: Optional[ControlButton] = None

    @staticmethod
    def __close_game() -> None:
        pg.quit()
        exit()

    def __click_button(self, buttons_list: list[Button]) -> None:
        for button in buttons_list:
            if button.rect.collidepoint(pg.mouse.get_pos()):
                if button.control_button:
                    button.control_button.selected = True
                    self.select_button: ControlButton = button.control_button
                self.game.status = button.input(self.game)

    def __screensaver_event_handler(self, event: Event) -> None:
        if event.type == pg.KEYDOWN:
            self.game.status = Status.MAIN_MENU
            self.game.menu.dropdown_start_time = pg.time.get_ticks()

    def __main_menu_event_handler(self, event: Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.__click_button(self.game.menu.menu_buttons_list)

    def __exit_menu_event_handler(self, event: Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.__click_button(self.game.exit_menu.exit_buttons_list)

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.game.status = Status.MAIN_MENU
                self.game.exit_menu.exit_dropdown_start_time = pg.time.get_ticks()
            elif event.key == pg.K_RETURN:
                self.__close_game()

    def __settings_menu_event_handler(self, event: Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.__click_button(self.game.settings_menu.control_buttons_list)
            elif event.button == 4 or event.button == 5:
                self.game.settings_menu.scroll_menu(event.button)

        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.status = Status.MAIN_MENU

    def __control_menu_event_handler(self, event: Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.game.status = Status.SETTINGS
            else:
                self.select_button.set_new_key(event, game)
                self.select_button = None

    def event_loop(self) -> None:
        for event in pg.event.get():
            self.game.level.player.keyboard_input.keyboard_input(event)
            match event.type:
                case pg.QUIT:
                    self.__close_game()

            match self.game.status:  # todo menu event handler class
                case Status.SCREENSAVER:
                    self.__screensaver_event_handler(event)
                case Status.MAIN_MENU:
                    self.__main_menu_event_handler(event)
                case Status.SETTINGS:
                    self.__settings_menu_event_handler(event)
                case Status.SET_CONTROL:
                    self.__control_menu_event_handler(event)
                case Status.EXIT:
                    self.__exit_menu_event_handler(event)


class Game:
    def __init__(self, handler: EventHandler) -> None:
        # general setup _____________________________________________________________________________
        pg.mixer.pre_init(*audio.MIXER_SETTINGS)
        pg.init()
        self.screen: Surface = pg.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
            settings.FLAGS,
            settings.BIT_PER_PIXEL
        )
        # pg.display.set_icon(pg.image.load(settings.GAME_ICO))
        pg.display.set_caption(settings.GAME_TITLE)
        self.clock: Clock = pg.time.Clock()

        self.event_handler: EventHandler = handler
        self.event_handler.game = self

        # self.state: State = State.MAIN_MENU
        self.state: State = State.GAME

        # menu setup ________________________________________________________________________________
        self.status: Status = Status.SCREENSAVER

        self.main_sound: Sound = pg.mixer.Sound(random.choice(audio.MAIN_MENU_SOUND))
        self.main_sound.set_volume(audio.MAIN_MENU_VOLUME)
        self.toggle_music_flag: bool = True

        # initialize menu
        self.menu: Menu = Menu()
        self.exit_menu: ExitMenu = ExitMenu()
        self.settings_menu: SettingsMenu = SettingsMenu()
        self.screensaver_menu: ScreensaverMenu = ScreensaverMenu()

        self.particle_player = ParticlePlayer()

        self.menu_fps: int = settings.MENU_FPS

        pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEWHEEL])

        # game process setup ________________________________________________________________________
        self.game_canvas: Surface = pg.Surface(
            (gSettings.GAME_CANVAS_WIDTH, gSettings.GAME_CANVAS_HEIGHT)
        )

        self.game_fps: int = gSettings.GAME_FPS

        self.sprite_sheet: SpriteSheet = SpriteSheet(
            gSettings.PLAYER_SPRITE_SHEET_PATH, gSettings.PLAYER_SPRITE_METADATA_PATH
        )
        pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEWHEEL])

        self.previous_time: float = time.time()
        self.level: Level = Level(self, self.sprite_sheet)


    def simple_toggle_music(self) -> None:
        if self.toggle_music_flag:
            self.main_sound.play(loops=audio.MAIN_MENU_LOOPS)
            self.toggle_music_flag: bool = False

    def run_menu(self, status: Status) -> None:
        self.screensaver_menu.start_screensaver(status)
        # self.simple_toggle_music()
        if status != Status.SCREENSAVER:
            self.menu.display_menu(status, self.exit_menu, self.settings_menu)
        if status == Status.EXIT:
            self.exit_menu.display_exit_menu()
        elif status == Status.SETTINGS or self.status == Status.SET_CONTROL:
            self.settings_menu.display_settings_menu(status)

    def run(self) -> None:
        while True:
            dt: float = time.time() - self.previous_time
            self.previous_time: float = time.time()

            match self.state:
                case State.MAIN_MENU:
                    self.run_menu(self.status)
                case State.GAME:
                    self.level.run(dt)
                    self.screen.blit(self.level.game_canvas, (
                        self.level.player.keyboard_input.camera_x,
                        self.level.player.keyboard_input.camera_y
                    ))  # todo ref

            self.event_handler.event_loop()
            # debug(self.level.player.status, 1000, 20)
            pg.display.update()
            self.clock.tick(self.menu_fps)


if __name__ == "__main__":
    event_handler: EventHandler = EventHandler()
    game: Game = Game(event_handler)
    game.run()
