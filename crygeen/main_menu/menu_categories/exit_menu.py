import pygame as pg

from crygeen.main_menu.buttons import Button
from crygeen.main_menu.menu_categories.menu import Menu
from crygeen.main_menu.states import Status
from crygeen.settings import settings


class ExitMenu(Menu):
    def __init__(self):
        super().__init__()
        self.exit_buttons_list: list = []
        self._exit_list: list = settings.EXIT_LIST
        self.exit_dropdown_start_time: int = 0

        # exit buttons
        self._exit_button_x: tuple[int, int] = settings.EXIT_BUTTON_X
        self._exit_button_y: int = settings.EXIT_BUTTON_Y
        self._exit_button_position: str = settings.EXIT_BUTTON_POSITION
        self.__create_exit_buttons()

    def __create_exit_buttons(self) -> None:
        y: int = self._exit_button_y
        x_coords: tuple[int, int] = self._exit_button_x
        for index, title in enumerate(self._exit_list):
            button: Button = Button(
                title=title,
                x=x_coords[index],
                y=y,
                font_name=self.main_menu_font_name,
                font_size=self.main_menu_font_size,
                font_color=self.main_menu_font_color,
                position=self._exit_button_position,
                opacity_offset=self.button_opacity_offset,
                alpha=self.alpha,
                index=index,
                properties=self._exit_list[title]
            )
            self.exit_buttons_list.append(button)

    def exit_button_action(self, key: int) -> Status:  # todo doc
        match key:
            case pg.K_RETURN:
                pg.quit()
                exit()
            case pg.K_ESCAPE:
                self.dropdown_start_time = pg.time.get_ticks()
                return Status.MAIN_MENU

    def display_exit_menu(self) -> None:  # todo dev
        ###### del block ######
        rect = self.img.get_rect()
        self.img.set_alpha(128)
        self._display_surface.blit(self.img, rect)
        ########################

        for button in self.exit_buttons_list:
            button.fade_in_hover()
            self._display_surface.blit(button.surf, button.rect)