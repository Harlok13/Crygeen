from typing import Optional

import pygame as pg
from pygame import QUIT, KEYDOWN, KEYUP, Surface, MOUSEBUTTONDOWN
from pygame.event import Event
from pygame.time import Clock

from crygeen import audio
from crygeen.buttons import ControlButton, Button
from crygeen.menu import Menu, ExitMenu, ScreensaverMenu, SettingsMenu
from crygeen.particles import ParticlePlayer

from crygeen.settings import settings
from crygeen.states import Status, State


class EventHandler:
    def __init__(self) -> None:
        self.game: Optional[Game] = None

        self.select_button: Optional[ControlButton] = None

    @staticmethod
    def __close_game():
        pg.quit()
        exit()

    def __click_button(self, buttons_list):
        for button in buttons_list:
            if button.rect.collidepoint(pg.mouse.get_pos()):
                if button.control_button:
                    button.control_button.selected = True
                    self.select_button: ControlButton = button.control_button
                self.game.status = button.input(self.game)

    def __screensaver_event_handler(self, event: Event):
        if event.type == pg.KEYDOWN:
            self.game.status = Status.MAIN_MENU
            self.game.menu.dropdown_start_time = pg.time.get_ticks()

    def __main_menu_event_handler(self, event: Event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.__click_button(self.game.menu.menu_buttons_list)

    def __exit_menu_event_handler(self, event: Event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.__click_button(self.game.exit_menu.exit_buttons_list)

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.game.status = Status.MAIN_MENU
            elif event.key == pg.K_RETURN:
                self.__close_game()

    def __settings_menu_event_handler(self, event: Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.__click_button(self.game.settings_menu.control_buttons_list)
            elif event.button == 4 or event.button == 5:
                self.game.settings_menu.scroll_menu(event.button)

        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.status = Status.MAIN_MENU

    def __control_menu_event_handler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.game.status = Status.SETTINGS
            else:
                self.select_button.set_new_key(event, game)
                self.select_button = None

    def event_loop(self):
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.__close_game()

            match self.game.status:
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
        # general setup
        pg.mixer.pre_init(*audio.MIXER_SETTINGS)
        pg.init()
        # self.canvas: Surface = pg.Surface((settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        self.screen: Surface = pg.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
            settings.FLAGS,
            settings.BIT_PER_PIXEL
        )
        pg.display.set_caption(settings.GAME_TITLE)
        self.clock: Clock = pg.time.Clock()

        self.status: Status = Status.SCREENSAVER
        self.state: State = State.MAIN_MENU

        self.menu: Menu = Menu()
        self.menu.toggle_music(True)
        self.exit_menu: ExitMenu = ExitMenu()
        self.settings_menu: SettingsMenu = SettingsMenu()
        self.screensaver_menu: ScreensaverMenu = ScreensaverMenu()

        self.particle_player = ParticlePlayer()

        self.event_handler: EventHandler = handler
        self.event_handler.game = self

        # pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, pg.MOUSEWHEEL])

    def run_menu(self, status):
        self.screensaver_menu.start_screensaver(status)
        if status != Status.SCREENSAVER:
            self.menu.display_menu(status, self.exit_menu, self.settings_menu)
        if status == Status.EXIT:
            self.exit_menu.display_exit_menu()
        elif status == Status.SETTINGS or self.status == Status.SET_CONTROL:
            self.settings_menu.display_settings_menu(status)

    def run(self):
        while True:

            match self.state:
                case State.MAIN_MENU:
                    self.run_menu(self.status)
                case State.GAME:
                    self.screen.fill('blue')

            match self.status:
                case Status.NEW_GAME:
                    self.state = State.GAME
            self.particle_player.display_particle_menu_effect(self.screen, 20)
            self.event_handler.event_loop()

            pg.display.update()
            self.clock.tick(settings.MENU_FPS)


if __name__ == "__main__":
    event_handler: EventHandler = EventHandler()
    game: Game = Game(event_handler)
    game.run()
