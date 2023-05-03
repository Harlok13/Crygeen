import math
import random
from enum import Enum
from typing import Optional, Callable

import pygame as pg
from pydantic import BaseModel, validator
from pygame import Surface, Rect
from pygame.font import Font
from pygame.mixer import Sound

from crygeen import audio
from crygeen.settings import settings
from crygeen.support import import_folder, deprecated


class ButtonModel(BaseModel):
    title: str
    x: int
    y: int
    font_name: str
    font_size: int
    font_color: str | tuple = settings.STD_BUTTON_COLOR,
    position: str = 'topleft'
    alpha: int = 200
    opacity_offset: float = 1
    width: Optional[int] = None
    height: Optional[int] = None
    action: Optional[Callable] = None

    @validator('position')
    def check_position(cls, v):
        allowed_positions = {'center', 'topleft', 'topright', 'bottomleft', 'bottomright'}
        if v not in allowed_positions:
            raise ValueError(f'Position must be one of {", ".join(allowed_positions)}')
        return v


class Button:

    def __init__(self, **kwargs) -> None:
        """
        Initialize a button.
                    :param text: The text content of the button.
                    :param x: The x-coordinate of the button.
                    :param y: The y-coordinate of the button.
                    :param font_name: The font used for the button text.
                    :param font_size: The font size used for the button text.
                    :param font_color: The color of the button text.
                    :param position: can only take a value from this list: topleft,
                                     topright, center, bottomleft, bottomright
                    :param alpha: The start amount of the button alpha.
                    :param opacity_offset: The amount by which the alpha value changes on hover.
                    :param width: The width of the button surface (default is None).
                    :param height: The height of the button surface (default is None).
                    :param action: The function to be called when the button is clicked.
                    :param kwargs:
                    """
        button_data = ButtonModel(**kwargs)
        self.title: str = button_data.title
        self.x: int = button_data.x
        self.y: int = button_data.y
        self.font_name: str = button_data.font_name
        self.font_size: int = button_data.font_size
        self.font_color: str | tuple = button_data.font_color
        self.font: Font = self.__get_font(self.font_name, self.font_size)
        self.position: str = button_data.position
        self.alpha: int = button_data.alpha
        self.default_alpha: int = self.alpha
        self.opacity_offset: float = button_data.opacity_offset
        self.width: Optional[int] = button_data.width
        self.height: Optional[int] = button_data.height
        self.__action = button_data.action
        self.surf: Surface = self.__get_surface()
        self.rect: Rect = self.__get_rect()

    def __get_surface(self) -> Surface:
        """
        Create text surface and set start alpha value.
        :return:
        """
        text_surf: Surface = self.font.render(
            self.title, True, self.font_color
        )
        text_surf.set_alpha(self.default_alpha)
        return text_surf

    def __get_rect(self) -> Rect:
        """
        Create rect depending on position.
        :return:
        """
        if self.position == 'topleft':
            return self.surf.get_rect(topleft=(self.x, self.y))
        elif self.position == 'center':
            return self.surf.get_rect(center=(self.x, self.y))
        elif self.position == 'bottomleft':
            return self.surf.get_rect(bottomleft=(self.x, self.y))
        elif self.position == 'bottomright':
            return self.surf.get_rect(bottomright=(self.x, self.y))
        elif self.position == 'topright':
            return self.surf.get_rect(topright=(self.x, self.y))

    @staticmethod
    def __get_font(font_name: str, font_size: int) -> Font:
        """Setup font."""
        return pg.font.Font(font_name, font_size)

    def __is_selected(self) -> bool:
        """
        Notifies if the button is selected.
        :return: boolean
        """
        # mb im add keyboard also
        return self.rect.collidepoint(pg.mouse.get_pos())

    # TODO fix this
    def fade_in_hover(self) -> None:
        """
        Fade in the button on hover. The selected button gradually
        becomes brighter.
        :return:
        """
        if self.__is_selected():
            if self.alpha < 255:
                self.alpha += self.opacity_offset
                self.surf.set_alpha(self.alpha)

        else:
            if self.alpha > self.default_alpha:
                self.alpha -= self.opacity_offset
                self.surf.set_alpha(self.alpha)

    @deprecated
    def run(self):
        """
        Run in main loop.
        :return:
        """
        self.fade_in_hover()


class Menu:
    def __init__(self) -> None:
        # general setup
        # self.main_menu_font: Font = pg.font.Font(settings.MAIN_MENU_FONT, settings.MAIN_MENU_FONT_SIZE)
        self.main_menu_font_name: str = settings.MAIN_MENU_FONT
        self.main_menu_font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.main_menu_font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR
        self.main_menu_position: str = settings.MAIN_MENU_POSITION
        self._main_menu_list = settings.MAIN_MENU_LIST
        self._menu_surfaces: list[Surface] = []  # TODO del?
        self.opacity_offset: float = settings.MAIN_MENU_OPACITY_OFFSET
        self.alpha: int = settings.MAIN_MENU_ALPHA
        self._display_surface: Surface = pg.display.get_surface()
        self._screen_size: tuple[int, int] = self._display_surface.get_size()

        self.buttons_list = []
        self.__create_menu_buttons()

        # screensaver setup
        self.screensaver_active: bool = True
        self._screensaver_data: list[Surface] = self.__load_screensaver_data()
        self._count_frames: int = len(self._screensaver_data)
        self._screensaver_idx: int = 0
        self._screensaver_font_size: int = settings.SCREENSAVER_FONT_SIZE
        self._screensaver_font: Font = pg.font.Font(settings.SCREENSAVER_FONT, self._screensaver_font_size)
        self.shading_alpha: float = 255
        self.fading_alpha: float = 0

        # main theme setup
        self._music: bool = False
        self._main_sound: Sound = self.__set_menu_music()

        # settings section setup

    # supporting functions __________________________________________________________________________
    def __alpha_vanish(
            self,
            color: str | tuple = settings.SCREENSAVER_ALPHA_COLOR,
            reverse: bool = False,
            offset: float = settings.SCREENSAVER_ALPHA_OFFSET
    ) -> None:
        """
        Used to fade the screen in and out by adjusting the alpha value of a
        shading surface. If 'reverse' is set to 'True', then the screen fades
        out, otherwise it fades in. The 'offset' parameter determines how quickly
        the shading fades, and 'color' determines the color of the shading.
        # TODO ref
        :param color: A string or tuple representing the color of the shading surface.
                      Default value is 'settings.SCREENSAVER_ALPHA_COLOR'.
        :param reverse: A boolean value indicating whether the screen should fade out
                        ('True') or fade in ('False'). Default value is 'False'.
        :param offset: A float value representing the speed at which the shading fades.
                       Default value is 'settings.SCREENSAVER_ALPHA_OFFSET'.
        :return:
        """
        # shading
        if not reverse:
            self._fade_surface: Surface = pg.Surface(self._screen_size)
            self._fade_surface.fill(color)
            self._fade_surface.set_alpha(self.shading_alpha)  # type: ignore

            if self.shading_alpha > 0:
                self.shading_alpha -= offset
                if self.shading_alpha < 0:
                    self.shading_alpha = 0

                self._fade_surface.set_alpha(self.shading_alpha)
                self._display_surface.blit(self._fade_surface, (0, 0))
        # fading
        else:
            self._fade_surface: Surface = pg.Surface(self._screen_size)
            self._fade_surface.fill(color)
            self._fade_surface.set_alpha(self.fading_alpha)  # type: ignore

            if self.fading_alpha < 255:
                self.fading_alpha += offset
                if self.fading_alpha > 255:
                    self.fading_alpha = 255

                self._fade_surface.set_alpha(self.fading_alpha)
                self._display_surface.blit(self._fade_surface, (0, 0))

    def __draw_text(self, text: str, font: Font, surface: Surface, x: int, y: int) -> tuple[Rect, Surface]:
        """
        Draw a text on the screen.
        :param text: The text to be displayed.
        :param font: The font used for the text.
        :param surface: The Surface object on which the text will be drawn.
        :param x: The x-coordinate of the starting point of text display.
        :param y: The y-coordinate of the starting point of text display.
        :return:
        """
        text_obj: Surface = font.render(text, True, self.main_menu_font_color)
        text_rect: Rect = text_obj.get_rect()
        text_rect.center = (x, y)
        item_alpha: int = int(abs(math.sin(pg.time.get_ticks() / 1000)) * 128 + 128)
        text_obj.set_alpha(item_alpha)
        surface.blit(text_obj, text_rect)

        return text_rect, text_obj  # rudiment, refactor

    # music setup __________________________________________________________________________________
    def toggle_music(self, forcibly_set: Optional[bool] = None) -> None:
        """
        API for toggle music.
        If the argument is not specified, then the value is reversed,
        otherwise the value takes the value of the argument
        :param forcibly_set: If you need to get a specific value.
        :return:
        """
        self._main_sound: bool = (not self._music, forcibly_set)[bool(forcibly_set)]

    @staticmethod
    def __set_menu_music() -> Sound:
        """
        General setup music.
        Select one of the songs, set the volume and repeat cycle.
        :return: One random music in playlist.
        """
        main_sound: Sound = pg.mixer.Sound(random.choice(audio.MAIN_MENU_SOUND))
        main_sound.set_volume(audio.MAIN_MENU_VOLUME)
        main_sound.play(loops=audio.MAIN_MENU_LOOPS)
        return main_sound

    # screensaver setup ____________________________________________________________________________
    def __load_screensaver_data(self) -> list[Surface]:
        """
        Create list of screensaver surfaces and optimize size according to screen size.
        :return: List of surfaces needed for animation.
        """
        screensaver_data: list[Surface] = import_folder(settings.SCREENSAVER_PATH)

        screensaver_scale_data: list[Surface] = [pg.transform.scale(item, self._screen_size) for item in
                                                 screensaver_data]

        return screensaver_scale_data

    def __start_screensaver(self, state: 'State') -> None:
        """
        Draws a splash screen when the application starts.
        :return:
        """
        self._screensaver_idx: int = (self._screensaver_idx + 1) % self._count_frames

        self._display_surface.blit(self._screensaver_data[self._screensaver_idx], (0, 0))
        self.__alpha_vanish()

        # TODO relocate settings
        if state == State.SCREENSAVER:
            text = self.__draw_text(
                'Press any key to continue...',
                self._screensaver_font,
                self._display_surface,
                self._screen_size[0] // 2,
                600
            )

    @deprecated
    def __close_screensaver(self) -> None:
        """
        Draws a splash screen when the application closes
        :return:
        """
        self._screensaver_idx: int = (self._screensaver_idx - 1) % self._count_frames

        # main menu setup _______________________________________________________________________________

    # main menu setup _______________________________________________________________________________
    def __create_menu_buttons(self) -> None:
        """
        Creates the main menu buttons and add them to the buttons list.
        Сoords are set for the location of buttons on the screen.
        :return:
        """
        x: int = settings.MAIN_MENU_X
        y, y_offset = settings.MAIN_MENU_Y, settings.MAIN_MENU_Y_OFFSET

        for row in self._main_menu_list:
            y += y_offset
            button: Button = Button(
                title=title,
                x=x,
                y=y,
                font_name=self.main_menu_font_name,
                font_size=self.main_menu_font_size,
                font_color=self.main_menu_font_color,
                position=self.main_menu_position,
                opacity_offset=self.opacity_offset,
                alpha=self.alpha,
            )
            self.buttons_list.append(button)

    # in dev
    def start_menu_animation(self) -> None:
        """
        Play animation, when...
        :return:
        """
        for button in self.buttons_list:
            ...

    @deprecated
    def __text_effects(self) -> None:
        for i, item_surface in enumerate(self._menu_surfaces):
            item_alpha = int(abs(math.sin(pg.time.get_ticks() / 1000 + i)) * 128 + 128)
            item_surface.set_alpha(item_alpha)
            self._display_surface.blit(item_surface, (100, 100 + i * 50))

    @deprecated
    def __draw_menu(self, dt: float) -> None:
        # self.__draw_menu_text()
        # self.__text_effects()
        pass

    # settings section ______________________________________________________________________________

    # settings section end __________________________________________________________________________

    def display(self, state: 'State', dt: float) -> None:
        """
        Run menu im main loop.
        :param state: Current state.
        :param dt: Delta time.
        :return:
        """
        self.__start_screensaver(state)
        # sleep for a while
        if state == State.MAIN_MENU:  # TODO deprecated
            self.__draw_menu(dt)

    @deprecated
    def run(self):
        pass


class State(Enum):
    SCREENSAVER: str = 'SCREENSAVER'
    MAIN_MENU: str = 'MAIN_MENU'
    GAME: str = 'GAME'
    GAME_PAUSE: str = 'GAME_PAUSE'
