import pygame as pg
from pygame import Surface

from crygeen.game_process.game_settings import gSettings


class PlayerAnimation:
    def __init__(self, player):  # type: ('Player') -> None
        self.player = player
        self._frame_index: int = 0
        self._animation_speed: float = gSettings.PLAYER_ANIMATION_SPEED

    def play_animation(self, dt: float, status: str) -> None:
        self._frame_index += self._animation_speed * dt

        if self._frame_index >= self.player._sprite_sheet.data['frames'][f'{status}0.png']['animation_len']:
            self._frame_index: int = 0
        sprite: Surface = self.player._sprite_sheet.parse_sprite(f'{status}{int(self._frame_index)}.png')

        if self.player._sprite_sheet.data['frames'][f'{status}0.png'].get('reverse', False):
            sprite: Surface = pg.transform.flip(sprite, True, False)

        self.player.image = sprite
        self.player.rect = self.player.image.get_rect(center=self.player.hitbox.center)

    def render(self, dt: float, status: str) -> None:
        self.play_animation(dt, status)
