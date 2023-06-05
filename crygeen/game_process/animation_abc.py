from abc import ABC, abstractmethod, ABCMeta
from typing import Any

import pygame as pg
from pygame import Surface

from crygeen.game_process.game_settings import gSettings


class AnimationAbc(ABC):
    __metadata__ = ABCMeta

    def __init__(self, animation_speed: float = gSettings.STD_ANIMATION_SPEED) -> None:
        self._frame_index: int = 0
        self._animation_speed: float = animation_speed

    def entity_play_animation(cls, dt: float, status: str, entity: Any, *args, **kwargs) -> None:
        cls._frame_index += cls._animation_speed * dt

        if cls._frame_index >= entity.sprite_sheet.data['frames'][f'{status}0.png']['animation_len']:
            cls._frame_index: int = 0
        sprite: Surface = entity.sprite_sheet.parse_sprite(f'{status}{int(cls._frame_index)}.png')

        if entity.sprite_sheet.data['frames'][f'{status}0.png'].get('reverse', False):
            sprite: Surface = pg.transform.flip(sprite, True, False)

        entity.image = sprite
        entity.rect = entity.image.get_rect(center=entity.hitbox.center)

    def magic_play_animation(self, dt: float, magic_entity: Any) -> None:
        self._frame_index += self._animation_speed * dt

        if self._frame_index >= magic_entity.sprite_sheet.data['frames'][f'0.png']['animation_len']:
            self._frame_index: int = 0

        sprite: Surface = magic_entity.sprite_sheet.parse_sprite(f'{int(self._frame_index)}.png')

        magic_entity.image = sprite
        magic_entity.rect = magic_entity.image.get_rect()

    @abstractmethod
    def play_animation(self, dt: float, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def render(self, dt: float, *args, **kwargs) -> None:
        self.play_animation(dt, *args, **kwargs)
