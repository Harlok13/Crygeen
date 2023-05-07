import math
import operator
import random
from time import sleep
from typing import Optional, Callable

import pygame as pg
from pygame import Surface, Rect
from pygame.font import Font
from pygame.mixer import Sound

from crygeen import audio
from crygeen.buttons import Button
from crygeen.settings import settings
from crygeen.states import State, Status
from crygeen.support import import_folder, deprecated


class Menu:
    def __init__(self) -> None:
        # general setup _____________________________________________________________________________
        self._display_surface: Surface = pg.display.get_surface()  # TODO deprecated
        self._screen_size: tuple[int, int] = self._display_surface.get_size()

        # menu setup ________________________________________________________________________________
        self.main_menu_font_name: str = settings.MAIN_MENU_FONT
        self.main_menu_font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.main_menu_font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR
        self.main_menu_position: str = settings.MAIN_MENU_POSITION
        self._main_menu_list = settings.MAIN_MENU_LIST
        self.alpha: int = settings.MAIN_MENU_ALPHA
        self.opacity_offset: float = settings.MAIN_MENU_OPACITY_OFFSET  # TODO deprecated?

        # menu buttons setup
        self.buttons_list: list = []
        self._menu_y_dest_positions: list = []
        self.__create_menu_buttons()

        # dropdown menu effect
        self.animation_time = 2000  # TODO reloc to settings
        self.dropdown_start_time: int = 0  # get value, when change state  # TODO fix to status?

        # screensaver setup _________________________________________________________________________
        self.screensaver_active: bool = True
        # opacity effect
        self._screensaver_flag: bool = False
        self._screensaver_start_time: int = 0  # get value, when first start
        self._screensaver_alpha_vanish_duration: int = settings.SCREENSAVER_ALPHA_VANISH_DURATION

        self._screensaver_data: list[Surface] = self.__load_screensaver_data()
        self._count_frames: int = len(self._screensaver_data)
        self._screensaver_frame_idx: int = 0
        self._screensaver_font_size: int = settings.SCREENSAVER_FONT_SIZE
        self._screensaver_font: Font = pg.font.Font(settings.SCREENSAVER_FONT, self._screensaver_font_size)

        # main theme setup __________________________________________________________________________
        self._music: bool = False
        self._main_sound: Sound = self.__set_menu_music()

        # exit section setup ________________________________________________________________________
        self.exit_buttons_list: list = []
        self._exit_list: list = settings.EXIT_LIST
        self.exit_dropdown_start_time: int = 0  # get value, when status = exit
        self._exit_width: int = self._screen_size[0] // 2
        self._exit_height: int = self._screen_size[1] // 2

        # exit buttons
        self.__create_exit_buttons()  # TODO reloc

        # garbage ___________________________________________________________________________________
        self.img = pg.image.load('setting_bg6.jpeg').convert_alpha()

        # settings section __________________________________________________________________________
        self.control_list: dict = settings.CONTROL
        self._control_buttons_list: list = []
        self._control_y_dest_positions: list = []

        self.__create_settings_buttons()
        self.settings_dropdown_start_time = 0
        self.settings_alpha_vanish_duration = settings.SETTINGS_ALPHA_VANISH_DURATION

    # settings section ______________________________________________________________________________
    def __create_settings_buttons(self) -> None:  # TODO remove code duplications
        # params: return tuple with buttons and dest pos
        x: int = settings.CONTROL_X
        y, y_offset = settings.CONTROL_Y, settings.CONTROL_Y_OFFSET
        dest_pos_y = y
        for index, title in enumerate(self.control_list):
            dest_pos_y += y_offset
            button: Button = Button(
                title=title,
                x=x,
                y=y,
                font_name=self.main_menu_font_name,
                font_size=settings.CONTROL_FONT_SIZE,
                font_color=self.main_menu_font_color,
                position=self.main_menu_position,
                opacity_offset=self.opacity_offset,
                alpha=self.alpha,
                index=index,
                properties=''
            )
            self._control_y_dest_positions.append(dest_pos_y)
            self._control_buttons_list.append(button)

    def __display_settings_menu(self, status) -> None:
        self.__alpha_vanish(1000, self.settings_dropdown_start_time, 0, 128, self.settings_fade_surf)  # TODO ref
        self.__dropdown_menu_effect(self._control_buttons_list, self.settings_dropdown_start_time, self.animation_time,
                                    self._control_y_dest_positions)

        for button in self._control_buttons_list:
            button.fade_in_hover()

            self._display_surface.blit(button.surf, button.rect)

    # exit section __________________________________________________________________________________
    def __create_exit_buttons(self) -> None:  # todo ref all!
        y: int = settings.EXIT_BUTTON_Y
        x_coords: tuple[int, int] = settings.EXIT_BUTTON_X
        position: str = settings.EXIT_BUTTON_POSITION
        for index, title in enumerate(self._exit_list):
            button: Button = Button(
                title=title,
                x=x_coords[index],
                y=y,
                font_name=self.main_menu_font_name,
                font_size=self.main_menu_font_size,
                font_color=self.main_menu_font_color,
                position=position,
                opacity_offset=self.opacity_offset,
                alpha=self.alpha,
                index=index,
                properties=self._exit_list[title]
            )
            self.exit_buttons_list.append(button)

    def __display_exit_menu(self) -> None:
        ###### del block######
        rect = self.img.get_rect()
        self.img.set_alpha(128)
        self._display_surface.blit(self.img, rect)
        for button in self.exit_buttons_list:
            button.fade_in_hover()
            self._display_surface.blit(button.surf, button.rect)

    # supporting functions __________________________________________________________________________
    def __alpha_vanish(
            self,
            duration: int,
            start_time: int,
            start_alpha: int,
            end_alpha: int,
            surface: Surface,
            color: str | tuple = settings.SCREENSAVER_SURF_COLOR,
    ) -> None:
        """
        Used to fade the screen in and out by adjusting the alpha value of a
        shading surface. If 'reverse' is set to 'True', then the screen fades
        out, otherwise it fades in. The 'offset' parameter determines how quickly
        the shading fades, and 'color' determines the color of the shading.
        :param duration: Animation play time.
        :param start_time: The time at which the screen should start fading.
        :param color: A string or tuple representing the color of the shading surface.
                      Default value is 'settings.SCREENSAVER_ALPHA_COLOR'.
        :param reverse: A boolean value indicating whether the screen should fade out
                        ('True') or fade in ('False'). Default value is 'False'.
        :return:  # TODO ref doc
        """
        op: Callable = (operator.lt, operator.gt)[start_alpha > end_alpha]

        surface.fill(color)
        delta: int = pg.time.get_ticks() - start_time
        erp_alpha: float = self.__lerp(start_alpha, end_alpha, delta / duration)
        if op(erp_alpha, end_alpha):  # < or >
            surface.set_alpha(erp_alpha)  # type: ignore
        self._display_surface.blit(surface, (0, 0))

    def __dropdown_menu_effect(
            self,
            buttons_list: list[Button],
            start_time: int,
            animation_time: int,
            y_dest_positions: list[int],
            reverse_opacity: bool = False
    ) -> None:
        """
        Play animation, when open menu.
        self.animation_time: The duration of the animation.
        delta: The time elapsed since the function was called.
        :return:  # TODO refactor doc and reloc to support func
        """
        opacity_values = (self.alpha, 0) if reverse_opacity else (0, self.alpha)
        if animation_time > 0:
            delta: int = pg.time.get_ticks() - start_time
            for button in buttons_list:
                if delta < animation_time:
                    button.rect.y = self.__lerp(
                        button.rect.y, y_dest_positions[button.index], delta / animation_time
                    )
                    button.surf.set_alpha(self.__lerp(
                        *opacity_values, delta / animation_time
                    ))

    def __draw_text(  # TODO ref all
            self,
            text: str,
            font: Font,
            surface: Surface,
            x: int,
            y: int,
            emergence: bool = False,
            text_effect: bool = False,
    ) -> tuple[Rect, Surface]:
        """
        Draw a text on the screen.
        :param text: The text to be displayed.
        :param font: The font used for the text.
        :param surface: The Surface object on which the text will be drawn.
        :param x: The x-coordinate of the starting point of text display.
        :param y: The y-coordinate of the starting point of text display.
        :param emergence: If the text should be smoothly emerging.
        :param text_effect: If the text should be animated.
        :return:
        """
        text_obj: Surface = font.render(text, True, self.main_menu_font_color)
        text_rect: Rect = text_obj.get_rect()
        text_rect.center = (x, y)
        if emergence:  # TODO ref hard code
            delta = pg.time.get_ticks() - self._screensaver_start_time
            x: float | int = self.__lerp(
                0, 255, delta / 7000
            )

            if x < 200:
                text_obj.set_alpha(x)
            else:
                if text_effect:
                    self.__add_text_effect(text_obj)

        surface.blit(text_obj, text_rect)

        return text_rect, text_obj  # rudiment, refactor

    @staticmethod
    def __lerp(a: float, b: float, t: float) -> float | int:
        """
        Linear interpolation formula.
        The formula is used to smoothly change the start and end values of
        coordinates, and modify this value based on the time 't' elapsed
        since the start of the movement.
        :param a: The starting value.
        :param b: The ending value.
        :param t: The interpolation factor, ranging from 0 to 1.
        :return: The interpolated value between a and b based on the factor 't'.
        """
        return a + (b - a) * t

    @staticmethod
    def __add_text_effect(obj: Surface):
        item_alpha: int = int(abs(math.sin(pg.time.get_ticks() / 1000)) * 128 + 128)
        obj.set_alpha(item_alpha)

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

    def __start_screensaver(self, status: Status) -> None:
        """
        Draws a splash screen when the application starts.
        :return:
        """
        if not self._screensaver_flag:  # get time for lerp and start animation
            self._screensaver_start_time: int = pg.time.get_ticks()
            self._screensaver_flag: bool = True
        self._screensaver_frame_idx: int = (self._screensaver_frame_idx + 1) % self._count_frames

        self._display_surface.blit(self._screensaver_data[self._screensaver_frame_idx], (0, 0))

        self.__alpha_vanish(self._screensaver_alpha_vanish_duration, self._screensaver_start_time, 255, 0,
                            self.screensaver_fade_surf)  # TODO ref hard code

        if status == Status.SCREENSAVER:
            self.__draw_text(
                'Press any key to continue...',
                self._screensaver_font,
                self._display_surface,
                self._screen_size[0] // 2,
                600,
                text_effect=True,
                emergence=True
            )

    # main menu setup _______________________________________________________________________________
    def __create_menu_buttons(self) -> None:
        """
        Creates the main menu buttons and add them to the buttons list.
        Сoords are set for the location of buttons on the screen.
        :return:
        """
        x: int = settings.MAIN_MENU_X
        y, y_offset = settings.MAIN_MENU_Y, settings.MAIN_MENU_Y_OFFSET
        dest_pos_y = y
        for index, title in enumerate(self._main_menu_list):
            dest_pos_y += y_offset
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
                index=index,
                properties=self._main_menu_list[title]
            )
            self._menu_y_dest_positions.append(dest_pos_y)
            self.buttons_list.append(button)

    def __display_menu_buttons(self, status: Status):
        """
        Displays menu buttons on the screen based on the application state.
        If the application state is 'State.MAIN_MENU', the method starts the menu
        animation and displays all menu buttons. If the mouse is hovering
        over a button, it "fades in" using the 'fade_in_hover' method,
        otherwise it returns to its original value.
        :return:
        """
        if status == status.MAIN_MENU:
            self.__dropdown_menu_effect(
                self.buttons_list, self.dropdown_start_time, self.animation_time, self._menu_y_dest_positions
            )
        if status != status.MAIN_MENU:
            self.__dropdown_menu_effect(
                self.buttons_list, self.exit_dropdown_start_time, self.animation_time, [1000, 1000, 1000, 1000], True
            )

        if status != Status.SETTINGS:  # TODO fix don't work correctly
            print('da')
            self.__dropdown_menu_effect(self._control_buttons_list, self.settings_dropdown_start_time,
                                        self.animation_time, [1000] * len(self._control_buttons_list), True)
            # for button in self._control_buttons_list:
            #     self._display_surface.blit(button.surf, button.rect)

        for button in self.buttons_list:
            button.fade_in_hover()

            self._display_surface.blit(button.surf, button.rect)

    # run on main loop ______________________________________________________________________________
    def run(self, status: Status) -> None:
        """
        Run menu im main loop.
        :param status: Current status.
        :return:
        """
        self.__start_screensaver(status)
        if status != Status.SCREENSAVER:
            self.__display_menu_buttons(status)
        if status == Status.EXIT:
            self.__display_exit_menu()
        if status == Status.SETTINGS:
            self.__display_settings_menu(status)
