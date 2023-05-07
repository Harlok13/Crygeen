from pathlib import Path
from typing import Optional

import pygame as pg
from pygame import QUIT, KEYDOWN, KEYUP, Surface, MOUSEBUTTONDOWN
from pygame.time import Clock

from crygeen import audio
from crygeen.menu import Menu

from crygeen.settings import settings
from crygeen.states import Status, State


class EventHandler:
    def __init__(self) -> None:
        self.game: Optional[Game] = None

    @staticmethod
    def __close_game():
        pg.quit()
        exit()

    def event_loop(self):
        for event in pg.event.get():

            match event.type:
                case pg.QUIT:
                    self.__close_game()

                case pg.KEYDOWN:
                    if self.game.status == Status.EXIT:
                        self.game.status = self.game.menu.exit_button_action(event.key)
                    if self.game.status == Status.SCREENSAVER:
                        self.game.status = Status.MAIN_MENU
                        self.game.menu.dropdown_start_time = pg.time.get_ticks()
                    if self.game.status == Status.SETTINGS:
                        self.game.menu.dropdown_start_time = pg.time.get_ticks()

                case pg.MOUSEBUTTONDOWN:  # TODO bag with scroll on buttons (fix)
                    if self.game.status == Status.SETTINGS:
                        self.game.menu.scroll_menu(event.button)

                    if self.game.state == State.MAIN_MENU:
                        for button in self.game.menu.menu_buttons_list:
                            if button.rect.collidepoint(pg.mouse.get_pos()):
                                self.game.status = button.input()
                                if self.game.status == Status.EXIT:
                                    self.game.menu.exit_dropdown_start_time = pg.time.get_ticks()
                                elif self.game.status == Status.SETTINGS:
                                    self.game.menu.settings_dropdown_start_time = pg.time.get_ticks()

                    if self.game.status == Status.EXIT:
                        for button in self.game.menu.exit_buttons_list:
                            if button.rect.collidepoint(pg.mouse.get_pos()):
                                self.game.status = button.input()
                                if self.game.status == Status.MAIN_MENU:
                                    self.game.menu.dropdown_start_time = pg.time.get_ticks()


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

        self.status = Status.SCREENSAVER
        self.state = State.MAIN_MENU

        self.menu: Menu = Menu()
        self.menu.toggle_music(True)

        self.event_handler: Optional[EventHandler] = handler
        self.event_handler.game = self

        self.control_data_path: Path = settings.CONTROL_DATA_PATH

        pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, pg.MOUSEWHEEL])

    def run(self):
        while True:

            match self.state:
                case State.MAIN_MENU:
                    self.menu.run(self.status)
                case State.GAME:
                    self.screen.fill('blue')

            match self.status:
                case Status.NEW_GAME:
                    self.state = State.GAME

            self.event_handler.event_loop()

            pg.display.update()
            self.clock.tick(settings.MENU_FPS)


if __name__ == "__main__":
    event_handler: EventHandler = EventHandler()
    game: Game = Game(event_handler)
    game.run()
