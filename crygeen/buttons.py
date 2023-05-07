import operator
from pathlib import Path
from typing import Optional, Callable

import pygame as pg
from pydantic import BaseModel, validator, FilePath
from pygame import Surface, Rect
from pygame.font import Font

from crygeen.settings import settings


class ButtonModel(BaseModel):
    title: str
    x: int
    y: int
    font_name: FilePath
    font_size: int
    font_color: str | tuple = settings.STD_BUTTON_COLOR,
    position: str = 'topleft'
    alpha: int = settings.STD_BUTTON_ALPHA
    opacity_offset: float = settings.STD_BUTTON_OPACITY_OFFSET
    width: Optional[int] = None
    height: Optional[int] = None
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
                    :param kwargs:
                    """
        button_data = ButtonModel(**kwargs)
        self.title: str = button_data.title
        self.x: int = button_data.x
        self.y: int = button_data.y
        self.font_name: Path = button_data.font_name
        self.font_size: int = button_data.font_size
        self.font_color: str | tuple = button_data.font_color
        self.font: Font = self.__get_font(self.font_name, self.font_size)
        self.position: str = button_data.position
        self.alpha: int = button_data.alpha
        self.default_alpha: int = self.alpha
        self.opacity_offset: float = button_data.opacity_offset
        self.width: Optional[int] = button_data.width
        self.height: Optional[int] = button_data.height
        self.surf: Surface = self.set_surface(self.title)
        self.rect: Rect = self.set_rect(self.position)

        self.index = kwargs['index']  # TODO doc new field
        self.properties = kwargs['properties']  # TODO doc new field

    def input(self):
        """
        Handle input events.
        :return:
        """
        exec(self.properties.get('action', 'print("no action")'))
        return self.properties.get('status')

    def set_surface(self, title) -> Surface:
        """
        Create text surface and set start alpha value.
        :return:
        """
        text_surf: Surface = self.font.render(
            title, True, self.font_color
        )
        return text_surf

    def set_scroll_opacity(self):  # todo ref all
        height: int = settings.SCREEN_HEIGHT
        boundary: int = height // 4
        start_y: int = 0 + boundary  # 100
        end_y: int = height - boundary  # 700
        half: int = height // 2
        y_percent: float = (half - start_y) / 100

        start_alpha: int = 200
        boundary_alpha: int = 50
        delta_alpha: int = start_alpha - boundary_alpha  # 100
        alpha_percent: float = 3  # delta_alpha / 100  # 1.5

        current_pos: int = abs(half - self.rect.y)
        current_alpha: float = current_pos * y_percent / alpha_percent

        if boundary_alpha <= current_alpha <= start_alpha:
            self.surf.set_alpha(operator.sub(start_alpha, current_alpha))

    def set_rect(self, position) -> Rect:
        """
        Create rect depending on position.
        :return:
        """
        match position:
            case 'topleft':
                return self.surf.get_rect(topleft=(self.x, self.y))
            case 'center':
                return self.surf.get_rect(center=(self.x, self.y))
            case 'bottomleft':
                return self.surf.get_rect(bottomleft=(self.x, self.y))
            case 'bottomright':
                return self.surf.get_rect(bottomright=(self.x, self.y))
            case 'topright':
                return self.surf.get_rect(topright=(self.x, self.y))

    @staticmethod
    def __get_font(font_name: Path, font_size: int) -> Font:
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
        :return:
        """
        if self.__is_selected():  # TODO ref dublicate
            op: Callable = (operator.iadd, operator.isub)[self.__is_selected()]
            if self.alpha < 255:
                self.alpha += self.opacity_offset
                self.font_color = (
                    255, self.font_color[1] - self.opacity_offset, self.font_color[2] - self.opacity_offset)
                self.surf = self.set_surface(self.title)
                self.surf.set_alpha(self.alpha)
        else:
            if self.alpha > self.default_alpha:
                self.alpha -= self.opacity_offset
                self.font_color = (
                    255, self.font_color[1] + self.opacity_offset, self.font_color[2] + self.opacity_offset)
                self.surf = self.set_surface(self.title)
                self.surf.set_alpha(self.alpha)

    def __repr__(self):
        return f"Button('{self.title}, {self.surf}, {self.rect}')"

    def __str__(self):
        return f'{self.title}'


class ControlButton(Button):
    def __init__(self):
        super().__init__()
        # dev


class Node:
    def __init__(self, button, prev_node=None, next_node=None):
        self.button = button
        self.prev = prev_node
        self.next = next_node

    def __str__(self):
        return f'{self.button}'


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, button):
        new_node = Node(button, self.tail, None)
        if self.tail is not None:
            self.tail.next = new_node

        else:
            self.head = new_node
        self.tail = new_node

    def prepend(self, button):
        new_node = Node(button, None, self.head)
        if self.head is not None:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node

    def insert_after_node(self, node, button):
        if node is None:
            return
        new_node = Node(button, node, node.next)
        if node.next is not None:
            node.next.prev = new_node
        else:
            self.tail = new_node
        node.next = new_node

    def delete_node(self, node_to_del):
        if node_to_del.prev is not None:
            node_to_del.prev.next = node_to_del.next
        else:
            # node_to_del is head node
            self.head = node_to_del.next

        if node_to_del.next is not None:
            node_to_del.next.prev = node_to_del.prev
        else:
            # node_to_del is tail node
            self.tail = node_to_del.prev

    def search_by_index(self, index):
        current_node = self.head
        while current_node is not None and index > 0:
            current_node = current_node.next
            index -= 1
        if current_node is not None:
            return current_node.button
        else:
            return None

    def set_y_offset(self, y_offset):
        current_node = self.head
        while current_node is not None:
            current_node.button.rect.y += y_offset
            current_node.button.set_scroll_opacity()
            current_node = current_node.next
