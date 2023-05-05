import pygame as pg
from pygame import QUIT, KEYDOWN, KEYUP, Surface, MOUSEBUTTONDOWN
from pygame.time import Clock

from crygeen import audio
from crygeen.controls import ControlsHandler
from crygeen.menu import Menu, State

from crygeen.settings import settings
from crygeen.states import Status
from crygeen.util import load_save, reset_keys


class Game:
    def __init__(self):
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
        # self.state = State.START_GAME

        self.menu: Menu = Menu()
        self.menu.toggle_music(True)

        self.control_data_path: str = settings.CONTROL_DATA_PATH

        pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN])

    def __event_loop(self):
        """
        Main pygame event loop. Toggle states.
        :return:
        """
        for event in pg.event.get():
            # TODO create event data (dict)
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            # drop screensaver
            elif event.type == pg.KEYDOWN and self.status == Status.SCREENSAVER:
                self.status = Status.MAIN_MENU
                # start dropdown menu effect
                self.menu.dropdown_start_time = pg.time.get_ticks()

            # exit status
            elif event.type == pg.KEYDOWN and self.status == Status.EXIT:
                if event.key == pg.K_RETURN:
                    pg.quit()
                    exit()
                elif event.key == pg.K_ESCAPE:
                    self.status = Status.MAIN_MENU
                    self.menu.dropdown_start_time = pg.time.get_ticks()

            elif event.type == pg.MOUSEBUTTONDOWN:

                if self.state == State.MAIN_MENU:
                    for button in self.menu.buttons_list:
                        if button.rect.collidepoint(pg.mouse.get_pos()):
                            self.status = button.input()
                            if self.status == Status.EXIT:
                                self.menu.exit_dropdown_start_time = pg.time.get_ticks()  # TODO change title
                            elif self.status == Status.SETTINGS:
                                self.menu.settings_dropdown_start_time = pg.time.get_ticks()

                if self.status == Status.EXIT:
                    for button in self.menu.exit_buttons_list:
                        if button.rect.collidepoint(pg.mouse.get_pos()):
                            self.status = button.input()
                            if self.status == Status.MAIN_MENU:
                                self.menu.dropdown_start_time = pg.time.get_ticks()

    def run(self):
        while True:

            self.__event_loop()
            # set menu
            if self.state == State.MAIN_MENU:
                self.menu.run(self.status)

            if self.status == Status.NEW_GAME:
                self.state = State.GAME
            if self.state == State.GAME:
                self.screen.fill('blue')

            # self.screen.blit(pg.transform.scale(self.canvas, self.screen.get_size()), (0, 0))
            pg.display.update()
            self.clock.tick(settings.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
