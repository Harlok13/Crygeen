"""
 #####
##    #
##        ######   ##    ##  ######    ######    ######   ######
##       ##    ##  ##   ##  ##    ##  ##    ##  ##    ##  ##   ##
##       ##         ## ##   ##    ##  ########  ########  ##    ##
##       ##           ##      #####   ##        ##        ##    ##
##    #  ##          ##         ##    ##     #  ##     #  ##    ##
 ####    ##         ##         ##      ######    ######   ##    ##
"""
import time
from typing import Optional

import pygame as pg
from pygame import QUIT, KEYDOWN, KEYUP, Surface, MOUSEBUTTONDOWN, MOUSEWHEEL
from pygame.time import Clock

from crygeen import audio
from crygeen.game_process.game_event_handler import GameEventHandler
from crygeen.game_process.game_process_setup import GameProcessSetup
from crygeen.main_menu.menu_event_handler import MenuEventHandler
from crygeen.main_menu.main_menu_setup import MainMenuSetup
from crygeen.main_menu.states import Status, State
from crygeen.settings import settings
from crygeen.utils.debug import debug


class EventHandler:
    def __init__(self) -> None:
        self.game: Optional[Game] = None

        self.menu_event_handler: Optional[MenuEventHandler] = None
        self.game_event_handler: Optional[GameEventHandler] = None

    @staticmethod
    def close_game() -> None:
        pg.quit()
        exit()

    def event_loop(self) -> None:
        for event in pg.event.get():

            match event.type:
                case pg.QUIT:
                    self.close_game()

            # player events
            self.game_event_handler.game_process.level.player.keyboard_input.keyboard_input(event)

            # main_menu events
            self.menu_event_handler.handlers.get(self.game.main_menu.menu_player.status)(event)


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

        # set game icon
        self.__ico: Surface = pg.image.load(settings.GAME_ICO).convert_alpha()
        self.__ico.set_colorkey((255, 255, 255))
        pg.display.set_icon(self.__ico)

        pg.display.set_caption(settings.GAME_TITLE)

        # time setup
        self.clock: Clock = pg.time.Clock()
        self.__previous_time: float = time.time()

        # self.state: State = State.MAIN_MENU
        self.state: State = State.GAME

        # main_menu setup
        self.main_menu: MainMenuSetup = MainMenuSetup()

        # game process setup
        self.game_process: GameProcessSetup = GameProcessSetup()

        # event handler setup
        self.__event_handler: EventHandler = handler
        self.__event_handler.game = self

        self.__menu_event_handler: MenuEventHandler = MenuEventHandler(
            self.main_menu, self.__event_handler.close_game, self)
        self.__event_handler.menu_event_handler = self.__menu_event_handler

        self.__game_event_handler: GameEventHandler = GameEventHandler(self.game_process)
        self.__event_handler.game_event_handler = self.__game_event_handler

    def __toggle_fps(self) -> None:
        match self.state:
            case State.MAIN_MENU:
                self.main_menu.fps = settings.MENU_FPS
                assert self.main_menu.fps is not None
            case State.GAME:
                self.main_menu.fps = None

    def run(self) -> None:
        while True:
            dt: float = time.time() - self.__previous_time
            self.__previous_time: float = time.time()

            self.__toggle_fps()

            match self.state:
                case State.MAIN_MENU:
                    self.main_menu.run()
                case State.GAME:
                    self.game_process.level.run(dt)

            self.__event_handler.event_loop()
            debug(self.game_process.level.player.rect.center, 1000, 20)
            debug(self.game_process.level.player.rect, 1000, 50)
            # debug(self.game_process.level.obstacle_sprites., 1000, 50)
            pg.display.update()
            self.clock.tick(self.main_menu.fps or self.game_process.fps)


if __name__ == "__main__":
    event_handler: EventHandler = EventHandler()
    game: Game = Game(event_handler)

    game.run()
