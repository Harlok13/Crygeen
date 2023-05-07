import operator
from typing import Optional, Callable

import pygame as pg
from pydantic import BaseModel, validator
from pygame import Surface, Rect
from pygame.font import Font

from crygeen.settings import settings
from crygeen.support import deprecated
from crygeen.states import State, Status


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
    action: Optional[Callable] = None  # TODO deprecated
    index: int
    properties: dict

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
        self.__action = button_data.action  # TODO deprecated
        self.surf: Surface = self.__get_surface()
        self.rect: Rect = self.__get_rect()

        self.index = kwargs['index']  # TODO doc new field
        self.properties = kwargs['properties']  # TODO doc new field

    def input(self):
        """
        Handle input events.
        :return:
        """
        exec(self.properties.get('action', 'print("no action")'))
        return self.properties.get('status')

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
        return bool(self.rect.collidepoint(pg.mouse.get_pos()))

    def fade_in_hover(self) -> None:
        """
        Fade in the button on hover. The selected button gradually
        becomes brighter.
        :return:  # TODO upd doc
        """
        if self.__is_selected():  # TODO ref dublicate
            op: Callable = (operator.iadd, operator.isub)[self.__is_selected()]
            if self.alpha < 255:
                self.alpha += self.opacity_offset
                self.font_color = (
                    255, self.font_color[1] - self.opacity_offset, self.font_color[2] - self.opacity_offset)
                self.surf = self.__get_surface()
                self.surf.set_alpha(self.alpha)
        else:
            if self.alpha > self.default_alpha:
                self.alpha -= self.opacity_offset
                self.font_color = (
                    255, self.font_color[1] + self.opacity_offset, self.font_color[2] + self.opacity_offset)
                self.surf = self.__get_surface()
                self.surf.set_alpha(self.alpha)
