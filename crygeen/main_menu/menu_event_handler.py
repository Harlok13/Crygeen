from typing import Optional, Callable

import pygame as pg
from pygame.event import Event


from crygeen.main_menu.buttons import ControlButton, Button
from crygeen.main_menu.states import Status


class MenuEventHandler:
    def __init__(self, main_menu, close_game: Callable, game) -> None:
        self.select_button: Optional[ControlButton] = None

        self.game = game  # type: 'Game'

        self.main_menu = main_menu  # type: 'MainMenuSetup'
        self.__close_game: Callable = close_game

    def __click_button(self, buttons_list: list[Button]) -> None:
        for button in buttons_list:
            if button.rect.collidepoint(pg.mouse.get_pos()):
                if button.control_button:
                    button.control_button.selected = True
                    self.select_button: ControlButton = button.control_button
                self.main_menu.animation_player.status = button.input(self.main_menu, self.game)

    def screensaver_event_handler(self, event: Event) -> None:
        if event.type == pg.KEYDOWN:
            self.main_menu.animation_player.status = Status.MAIN_MENU
            self.main_menu.menu.dropdown_start_time = pg.time.get_ticks()

    def main_menu_event_handler(self, event: Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.__click_button(self.main_menu.menu.buttons_list)

    def exit_menu_event_handler(self, event: Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.__click_button(self.main_menu.exit_menu.buttons_list)

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.main_menu.animation_player.status = Status.MAIN_MENU
                self.main_menu.exit_menu.dropdown_start_time = pg.time.get_ticks()
            elif event.key == pg.K_RETURN:
                self.__close_game()

    def settings_menu_event_handler(self, event: Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.__click_button(self.main_menu.settings_menu.buttons_list)
            elif event.button == 4 or event.button == 5:
                self.main_menu.settings_menu.scroll_menu(event.button)

        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.main_menu.animation_player.status = Status.MAIN_MENU

    def control_menu_event_handler(self, event: Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.main_menu.animation_player.status = Status.SETTINGS
            else:
                self.select_button.set_new_key(event, self.main_menu)
                self.select_button = None
