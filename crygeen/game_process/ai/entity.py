from abc import ABC, ABCMeta, abstractmethod

import pygame as pg
from pygame import Surface, Vector2, Rect
from pygame._sprite import Group

from crygeen.game_process.ai.kinematic_ai import NullNavigating
from crygeen.game_process.player_setup.player_direction import Direction
from crygeen.game_process.spritesheet import SpriteSheet
from crygeen.pygame_ai.steering.path import Path


class Entity(pg.sprite.Sprite):
    def __init__(
            self: 'Entity',
            group: Group,
            sprite_sheet_path: Path,
            sprite_metadata_path: Path,
            first_sprite_props: tuple[int, int, int, int],
            start_pos: Vector2,
            max_speed: int,
            max_acceleration: int,
            max_rotation: int,
            max_angular_acceleration: int
    ) -> None:

        super().__init__(group)  # noqa
        self.sprite_sheet: SpriteSheet = SpriteSheet(sprite_sheet_path, sprite_metadata_path)
        self.image: Surface = self.sprite_sheet.get_sprite(*first_sprite_props)

        self.rect: Rect = self.image.get_rect(center=start_pos)
        self.hitbox: Rect = self.rect

        self.velocity: Vector2 = Vector2(0, 0)
        self.max_speed: int = max_speed
        self.max_acceleration: int = max_acceleration

        self.orientation: int = 0
        self.rotation: int = 0
        self.max_rotation: int = max_rotation
        self.max_angular_acceleration: int = max_angular_acceleration

        self.ai: NullNavigating = NullNavigating()
        self.direction: Direction = Direction()

        self.status: str = 'down'
        self.prev_status: str = 'down_idle'

        self.prev_pos: Vector2 = pg.Vector2()
        self.prev_dir_vec: Vector2 = pg.Vector2()

        # self.dir_vec: Vector2 = (pg.Vector2(self.rect.center) - self.prev_pos).normalize_ip()
        self.dir_vec: Vector2 = pg.Vector2()

    @property
    def position(self) -> Vector2:
        return pg.Vector2(self.rect.center)

    @position.setter
    def position(self, pos: Vector2) -> None:
        self.rect.center = pos

    def navigate(self, navigating, dt):  # type: ('NavigatingOutput', float) -> None
        # change velocity
        self.velocity += navigating.linear * dt
        self.rotation += navigating.angular * dt

        # normalize vector
        if self.velocity.length() > self.max_speed:
            self.velocity.normalize_ip()
            self.velocity *= self.max_speed

    def round_direction(self, *dir_vectors):
        for dir_vec in dir_vectors:
            self.dir_vec.x = 0.7 if (
                                                self.dir_vec.x > 0 and self.dir_vec.x < 1) and self.dir_vec.x != 1 else self.dir_vec.x
            self.dir_vec.x = -0.7 if (
                                                 self.dir_vec.x < 0 and self.dir_vec.x > -1) and self.dir_vec.x != -1 else self.dir_vec.x

            self.dir_vec.y = 0.7 if (
                                                self.dir_vec.y > 0 and self.dir_vec.y < 1) and self.dir_vec.y != 1 else self.dir_vec.y
            self.dir_vec.y = -0.7 if (
                                                 self.dir_vec.y < 0 and self.dir_vec.y > -1) and self.dir_vec.y != -1 else self.dir_vec.y

    def update_direction_and_status(self):
        current_dir_vec = pg.Vector2(self.rect.center) - self.prev_pos

        if current_dir_vec.magnitude() != 0:
            current_dir_vec.normalize_ip()

        self.dir_vec = current_dir_vec

        self.round_direction(self.prev_dir_vec, current_dir_vec)

        # get status
        status: str = self.direction.get_direction_status(self.dir_vec, prev_direction=self.dir_vec)
        if self.dir_vec.magnitude() != 0:
            self.status: str = status.split('_')[0]
            self.prev_status: str = status
        else:
            self.status: str = self.prev_status

        # update previously position
        self.prev_pos: Vector2 = pg.Vector2(self.rect.center)

    def navigate_angular(self, navigating, dt):  # type: ('NavigatingOutput', int) -> None
        navigating_angular = navigating.copy()
        navigating_angular.linear.x = 0
        navigating_angular.linear.y = 0
        self.navigate(navigating_angular, dt)

    def get_lines(self):
        left = [self.rect.topleft, self.rect.bottomleft]
        top = [self.rect.topleft, self.rect.topright]
        right = [self.rect.topright, self.rect.bottomright]
        bottom = [self.rect.bottomright, self.rect.bottomleft]

        return [left, top, right, bottom]
