from typing import Optional

import pygame as pg
from pygame import Vector2
from pygame.event import Event
from pygame.key import ScancodeWrapper

from crygeen.game_process.game_settings import gSettings
from crygeen.game_process.player_setup.player_direction import Direction
from crygeen.game_process.player_setup.player_keyboard_logic import KeyboardLogic
from crygeen.main_menu.saver import SaveLoadManager
from crygeen.settings import settings


class PlayerKeyboardInput:
    def __init__(self, player):  # type: ('Player') -> None
        self.player = player  # type: 'Player'
        self.direction: Vector2 = pg.math.Vector2()
        self.control: dict[str, int] = self.__get_current_control()
        self.dir: Direction = Direction()
        self.keyboard_logic: KeyboardLogic = KeyboardLogic(self)

        self.status: str = 'down'
        self.prev: str = 'down'
        self.current_direction: str = 'down_idle'
        self.speed: int = gSettings.PLAYER_SPEED

        self.spurt_available: bool = True
        self.spurt_start_time: Optional[int] = None
        self.spurt_cd: int = gSettings.PLAYER_SPURT_CD
        self.spurt_duration: int = gSettings.PLAYER_SPURT_DURATION
        self.spurt_coefficient: float = gSettings.PLAYER_SPURT_COEFFICIENT

        self.attack_available: bool = True
        self.attack_start_time: Optional[int] = None
        self.attack_cd: int = gSettings.PLAYER_ATTACK_CD

        self.idle: bool = True

        self.lightning: bool = False

        self.camera_x: int = 0
        self.camera_y: int = 0

    def keyboard_input(self, event: Event) -> None:
        keys: ScancodeWrapper = pg.key.get_pressed()
        current_time: int = pg.time.get_ticks()

        if event.type == pg.KEYDOWN:
            if keys[self.control['Action']]:
                self.keyboard_logic.action()

        if True in keys:
            self.idle = False
            if 'attack' not in self.status:

                if keys[self.control['Up']]:
                    self.keyboard_logic.move_up()
                elif keys[self.control['Down']]:
                    self.keyboard_logic.move_down()
                else:
                    self.direction.y = 0

                if keys[self.control['Left']]:
                    self.keyboard_logic.move_left()
                elif keys[self.control['Right']]:
                    self.keyboard_logic.move_right()
                else:
                    self.direction.x = 0

            if keys[self.control['Spurt']]:
                self.keyboard_logic.spurt()

            if keys[pg.K_e]:
                self.lightning = True
        else:
            self.keyboard_logic.idle()
            self.lightning = False

    def __get_current_direction(self) -> None:
        if any(self.direction.xy):
            self.current_direction: str = self.dir.get_direction_status(self.direction)

    def __get_status(self) -> None:
        status: str = self.dir.get_direction_status(self.direction)
        if self.direction.xy != (0, 0):
            self.status: str = status.split('_')[0] if status else self.__get_prev_dir()

    def __get_prev_dir(self) -> None:
        self.prev: str = self.current_direction

    def __move(self, dt: float) -> None:
        if 'attack' not in self.status:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.player.hitbox.x += self.direction.x * self.speed * dt
            self.__collision(Direction.HORIZONTAL)

            self.player.hitbox.y += self.direction.y * self.speed * dt
            self.__collision(Direction.VERTICAL)

            self.camera_x -= self.direction.x * self.speed * dt  # todo ref
            self.camera_y -= self.direction.y * self.speed * dt

        self.player.rect.center = self.player.hitbox.center

    def __collision(self, direction: int) -> None:
        if direction == Direction.HORIZONTAL:
            for sprite in self.player.obstacle_sprites:
                if sprite.hitbox.colliderect(self.player.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.player.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:  # moving left
                        self.player.hitbox.left = sprite.hitbox.right

        if direction == Direction.VERTICAL:
            for sprite in self.player.obstacle_sprites:
                if sprite.hitbox.colliderect(self.player.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.player.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # moving up
                        self.player.hitbox.top = sprite.hitbox.bottom

    def __cooldowns(self) -> None:
        current_time = pg.time.get_ticks()

        # spurt cd __________________________________________________________________________________
        if not self.spurt_available:
            if current_time - self.spurt_start_time >= self.spurt_cd:
                self.spurt_available: bool = True
            if current_time - self.spurt_start_time >= self.spurt_duration:
                self.speed: int = gSettings.PLAYER_SPEED

        # attack cd _________________________________________________________________________________
        if not self.attack_available:
            if current_time - self.attack_start_time >= self.attack_cd:
                self.attack_available: bool = True
                self.status: str = self.current_direction.split('_')[0]

                if not self.idle:
                    self.direction.xy = self.dir.get_direction_vector(self.status)
                else:
                    self.idle = True
                    self.status: str = self.current_direction
                    self.direction.xy = (0, 0)

    @staticmethod
    def __get_current_control() -> dict[str, int]:
        loader: SaveLoadManager = SaveLoadManager()
        control_data: list[list[str, int, str]] = loader.load_save(settings.CONTROL_DATA_PATH)
        control: dict[str, int] = {title: constant for title, constant, _ in control_data}
        return control

    def update(self, dt: float) -> None:
        current_time = pg.time.get_ticks()
        self.__get_prev_dir()  # must be first
        self.__move(dt)  # must be second
        self.__get_current_direction()
        self.__get_status()

        self.__cooldowns()
