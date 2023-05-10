import math
import operator
import random
from functools import wraps
from pathlib import Path
from typing import Optional, Callable

import pygame as pg
from pygame import Surface, Rect
from pygame.font import Font
from pygame.mixer import Sound

from crygeen import audio
from crygeen.buttons import Button, LinkedList, ControlButton
from crygeen.controls import Key, Control
from crygeen.saver import SaveLoadManager
from crygeen.settings import settings
from crygeen.states import Status
from crygeen.support import import_folder_img


class Menu:
    def __init__(self) -> None:
        # general setup _____________________________________________________________________________
        self._display_surface: Surface = pg.display.get_surface()
        self._screen_size: tuple[int, int] = self._display_surface.get_size()
        self.save_load_manager: SaveLoadManager = SaveLoadManager()

        # menu setup ________________________________________________________________________________
        self.main_menu_font_name: str = settings.MAIN_MENU_FONT
        self.main_menu_font_size: int = settings.MAIN_MENU_FONT_SIZE
        self.main_menu_font_color: tuple[int, int, int] = settings.MAIN_MENU_FONT_COLOR
        self.main_menu_position: str = settings.MAIN_MENU_POSITION
        self._main_menu_list = settings.MAIN_MENU_LIST
        self.alpha: int = settings.MAIN_MENU_ALPHA
        self.button_opacity_offset: float = settings.MAIN_MENU_BUTTON_OPACITY_OFFSET

        # menu buttons setup
        self.menu_buttons_list: list = []
        self._menu_y_dest_positions: list = []
        self.__create_menu_buttons()

        # dropdown menu effect
        self.dropdown_animation_time = settings.MAIN_MENU_DROPDOWN_ANIMATION
        self.dropdown_start_time: int = 0

        # main theme setup __________________________________________________________________________
        self._music: bool = False
        self._main_sound: Sound = self.__set_menu_music()

        # garbage ___________________________________________________________________________________
        self.img = pg.image.load('assets/setting_bg6.jpeg').convert_alpha()

    # supporting functions __________________________________________________________________________
    def _alpha_vanish(
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
        erp_alpha: float = self._lerp(start_alpha, end_alpha, delta / duration)
        if op(erp_alpha, end_alpha):  # < or >
            surface.set_alpha(erp_alpha)  # type: ignore
        self._display_surface.blit(surface, (0, 0))

    def _dropdown_menu_effect(
            self,
            buttons_list: list[Button],
            start_time: int,
            animation_time: int,
            y_dest_positions: list[int],
            shading: bool = False
    ) -> None:
        """
        Play animation, when open menu.
        self.dropdown_animation_time: The duration of the animation.
        delta: The time elapsed since the function was called.
        :return:
        """
        opacity_values = (self.alpha, 0) if shading else (0, self.alpha)
        if animation_time > 0:
            delta: int = pg.time.get_ticks() - start_time
            for button in buttons_list:
                if delta < animation_time:
                    button.rect.y = self._lerp(
                        button.rect.y, y_dest_positions[button.index], delta / animation_time
                    )
                    button.surf.set_alpha(self._lerp(
                        *opacity_values, delta / animation_time
                    ))

    @staticmethod
    def _lerp(a: float, b: float, t: float) -> float | int:
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
    def _add_text_effect(obj: Surface):
        item_alpha: int = int(abs(math.sin(pg.time.get_ticks() / 1000)) * 128 + 128)
        obj.set_alpha(item_alpha)

    def _draw_text(self, text: str, font: Font, x: int, y: int) -> tuple[Rect, Surface]:
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

        return text_rect, text_obj

    def create_buttons(self, *, title, x, y, y_offset, list_of_buttons, font_name, font_size, font_color, position,
                       opacity_offset, alpha):
        x: int = settings.MAIN_MENU_X
        y, y_offset = settings.MAIN_MENU_Y, settings.MAIN_MENU_Y_OFFSET

        dest_pos_y = y
        for index, title in enumerate(list_of_buttons):
            dest_pos_y += y_offset
            button: Button = Button(
                title=title,
                x=x,
                y=y,
                font_name=font_name,
                font_size=font_size,
                font_color=font_color,
                position=position,
                opacity_offset=opacity_offset,
                alpha=alpha,
                index=index,
                properties=self._main_menu_list.get(title, None)
            )
            self._menu_y_dest_positions.append(dest_pos_y)
            self.menu_buttons_list.append(button)

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
                opacity_offset=self.button_opacity_offset,
                alpha=self.alpha,
                index=index,
                properties=self._main_menu_list[title]
            )
            self._menu_y_dest_positions.append(dest_pos_y)
            self.menu_buttons_list.append(button)

    def display_menu(self, status: Status, exit_menu, settings_menu):
        """
        Displays menu buttons on the screen based on the application state.
        If the application status is 'Status.MAIN_MENU', the method starts the menu
        animation and displays all menu buttons. If the mouse is hovering
        over a button, it "fades in" using the 'fade_in_hover' method,
        otherwise it returns to its original value.
        :return:
        """
        if status == Status.MAIN_MENU:
            self._dropdown_menu_effect(
                self.menu_buttons_list, self.dropdown_start_time, self.dropdown_animation_time,
                self._menu_y_dest_positions
            )
        if status != Status.MAIN_MENU:
            self._dropdown_menu_effect(
                self.menu_buttons_list, exit_menu.exit_dropdown_start_time, self.dropdown_animation_time,
                [1000] * len(self.menu_buttons_list), True
            )  # TODO ref hard code

        for button in self.menu_buttons_list:
            button.fade_in_hover()

            self._display_surface.blit(button.surf, button.rect)


class SettingsMenu(Menu):
    def __init__(self):
        super().__init__()
        self.linked_list: LinkedList = LinkedList()
        self.control_list: Control = settings.CONTROL
        self.control_buttons_list: list = []
        self._control_y_dest_positions: list = []
        self._control_buttons_position: str = settings.CONTROL_BUTTONS_POSITION
        self._control_bottom_boundary: int = settings.CONTROL_BOTTOM_BOUNDARY
        self._control_top_boundary: int = settings.CONTROL_TOP_BOUNDARY
        self._control_scroll_offset: int = settings.CONTROL_SCROLL_OFFSET

        # control buttons
        self.control_data_path: Path = settings.CONTROL_DATA_PATH
        self.__control_data: list[list[str, int, str]] = self.__load_control_data()

        self.__create_settings_buttons()

        # settings effects
        self.settings_fade_surf = pg.Surface(self._screen_size)
        self.settings_fade_surf.set_alpha(0)
        self.settings_dropdown_start_time: int = 0
        self._settings_alpha_vanish_duration = settings.SETTINGS_ALPHA_VANISH_DURATION
        self._settings_dest_alpha_vanish: int = settings.SETTINGS_DEST_ALPHA_VANISH
        self._control_animation_duration: int = settings.CONTROL_ANIMATION_DURATION

    def __create_settings_buttons(self) -> None:  # TODO remove code duplications
        # params: return tuple with buttons and dest pos
        x: int = settings.CONTROL_X
        y, y_offset = settings.CONTROL_Y, settings.CONTROL_Y_OFFSET  # todo ref
        dest_pos_y = y

        for index, key in enumerate(self.control_list):
            key: Key
            dest_pos_y += y_offset
            button_kwargs = {
                "title": f"{key.title}",
                "x": x,
                "y": y,
                "font_name": self.main_menu_font_name,
                "font_size": settings.CONTROL_FONT_SIZE,
                "font_color": self.main_menu_font_color,
                "position": self._control_buttons_position,
                "opacity_offset": self.button_opacity_offset,
                "alpha": self.alpha,
                "index": index,
                "properties": "",
            }
            button: Button = Button(
                **button_kwargs,
                control_button=ControlButton(title=f"{self.__control_data[index][2]}",
                                             x=1000,  # todo ref
                                             y=y,
                                             font_name=self.main_menu_font_name,
                                             font_size=settings.CONTROL_FONT_SIZE,
                                             font_color=self.main_menu_font_color,
                                             position='topright',
                                             opacity_offset=self.button_opacity_offset,
                                             alpha=self.alpha,
                                             index=index,
                                             properties="",
                                             constant=self.__control_data[index][1],  # type: ignore
                                             key=self.__control_data[index][2],

                                             )
            )
            self.linked_list.append(button)
            self._control_y_dest_positions.append(dest_pos_y)
            self.control_buttons_list.append(button)

    def scroll_menu_old(self, event_key: int) -> None:  # todo doc
        match event_key:
            case pg.SYSTEM_CURSOR_WAITARROW:
                if self.linked_list.head.button.rect.y <= self._control_bottom_boundary:
                    self.linked_list.set_y_offset(self._control_scroll_offset)

            case pg.SYSTEM_CURSOR_SIZENWSE:
                if self.linked_list.tail.button.rect.y >= self._control_top_boundary:
                    self.linked_list.set_y_offset(-self._control_scroll_offset)

    def scroll_menu(self, event_key: int) -> None:  # todo doc
        if event_key == 4:
            if self.linked_list.head.button.rect.y <= self._control_bottom_boundary:
                self.linked_list.set_y_offset(self._control_scroll_offset)

        elif event_key == 5:
            if self.linked_list.tail.button.rect.y >= self._control_top_boundary:
                self.linked_list.set_y_offset(-self._control_scroll_offset)

    def __load_control_data(self) -> list[list[str, int, str]]:
        try:
            return self.save_load_manager.load_save(self.control_data_path)
        except FileNotFoundError:
            self.save_load_manager.write_save(self.control_list, self.control_data_path)
            return self.save_load_manager.load_save(self.control_data_path)

    def display_settings_menu(self, status: Status) -> None:  # todo doc
        for button in self.control_buttons_list:
            button.set_scroll_opacity()
            button.control_button.set_scroll_opacity()
        self._alpha_vanish(self._settings_alpha_vanish_duration, self.settings_dropdown_start_time, 0,
                           self._settings_dest_alpha_vanish, self.settings_fade_surf)

        self._dropdown_menu_effect(self.control_buttons_list, self.settings_dropdown_start_time,
                                   self._control_animation_duration, self._control_y_dest_positions)

        control_list = [button.control_button for button in self.control_buttons_list]  # TODO fix this

        self._dropdown_menu_effect(control_list, self.settings_dropdown_start_time, self._control_animation_duration,
                                   self._control_y_dest_positions)

        if status == Status.SET_CONTROL:
            for button in self.control_buttons_list:
                if button.control_button.selected:
                    button.blinking_effect()
                    button.control_button.blinking_effect()

                self._display_surface.blit(button.surf, button.rect)
                self._display_surface.blit(button.control_button.surf, button.control_button.rect)
        else:

            for button in self.control_buttons_list:
                button.fade_in_hover()
                button.control_button.fade_in_hover()

                self._display_surface.blit(button.surf, button.rect)
                self._display_surface.blit(button.control_button.surf, button.control_button.rect)


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


class ScreensaverMenu(Menu):
    def __init__(self):
        super().__init__()
        self.screensaver_active: bool = True

        # opacity effect
        self._screensaver_flag: bool = False
        self.screensaver_fade_surf = pg.Surface(self._screen_size)
        self.screensaver_fade_surf.set_alpha(255)
        self._screensaver_dropdown_start_time: int = 0
        self._screensaver_alpha_vanish_duration: int = settings.SCREENSAVER_ALPHA_VANISH_DURATION
        self._screensaver_start_alpha_vanish: int = settings.SCREENSAVER_START_ALPHA_VANISH
        # text opacity effect
        self._screensaver_alpha_text_duration: int = settings.SCREENSAVER_ALPHA_TEXT_DURATION
        self._screensaver_start_text_alpha: tuple[int, int] = settings.SCREENSAVER_START_TEXT_ALPHA

        # screensaver bg
        self._screensaver_path: Path = settings.SCREENSAVER_PATH
        self._screensaver_data: list[Surface] = self.__load_screensaver_data()
        self._count_frames: int = len(self._screensaver_data)
        self._screensaver_frame_idx: int = 0

        # screensaver text
        self._screensaver_text: str = settings.SCREENSAVER_TEXT
        self._screensaver_font_size: int = settings.SCREENSAVER_FONT_SIZE
        self._screensaver_font: Font = pg.font.Font(settings.SCREENSAVER_FONT, self._screensaver_font_size)
        self._screensaver_text_x: int = self._screen_size[0] // 2 or settings.SCREENSAVER_TEXT_X
        self._screensaver_text_y: int = settings.SCREENSAVER_TEXT_Y

    def __load_screensaver_data(self) -> list[Surface]:
        """
        Create list of screensaver surfaces and optimize size according to screen size.
        :return: List of surfaces needed for animation.
        """
        screensaver_data: list[Surface] = import_folder_img(self._screensaver_path)

        screensaver_scale_data: list[Surface] = [pg.transform.scale(item, (1280, 800)) for item in
                                                 screensaver_data]  # TODO ref hard code

        return screensaver_scale_data

    def start_screensaver(self, status: Status) -> None:
        """
        Draws a splash screen when the application starts.
        :return:
        """
        if not self._screensaver_flag:
            self._screensaver_dropdown_start_time: int = pg.time.get_ticks()
            self._screensaver_flag: bool = True
        self._screensaver_frame_idx: int = (self._screensaver_frame_idx + 1) % self._count_frames

        self._display_surface.blit(self._screensaver_data[self._screensaver_frame_idx], (0, 0))

        self._alpha_vanish(self._screensaver_alpha_vanish_duration, self._screensaver_dropdown_start_time,
                           self._screensaver_start_alpha_vanish, 0, self.screensaver_fade_surf)

        if status == Status.SCREENSAVER:
            decorator = self._screensaver_text_effect(
                self._screensaver_start_text_alpha,
                self._screensaver_alpha_text_duration,
                self._screensaver_dropdown_start_time
            )(self._draw_text)

            text_rect, text_surf = decorator(
                text=self._screensaver_text,
                font=self._screensaver_font,
                x=self._screensaver_text_x,
                y=self._screensaver_text_y,
            )

            self._display_surface.blit(text_surf, text_rect)

    @staticmethod
    def _screensaver_text_effect(alpha_values: tuple[int, int], emergence_duration: int, start_time: int) -> Callable:
        def outer_wrapper(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                text_rect, text_surf = func(*args, **kwargs)

                delta: int = pg.time.get_ticks() - start_time
                start_alpha, end_alpha = alpha_values
                dt: float = delta / emergence_duration
                alpha_offset: float | int = start_alpha + (end_alpha - start_alpha) * dt

                if alpha_offset <= 200:
                    text_surf.set_alpha(alpha_offset)
                else:
                    wave_alpha: int = int(abs(math.sin(pg.time.get_ticks() / 1000)) * 128 + 128)
                    text_surf.set_alpha(wave_alpha)

                return text_rect, text_surf

            return wrapper

        return outer_wrapper
