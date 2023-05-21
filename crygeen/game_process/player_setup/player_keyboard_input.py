from typing import Optional

import pygame as pg
from pygame import Vector2
from pygame.event import Event
from pygame.key import ScancodeWrapper

from crygeen.game_process.game_settings import gSettings
from crygeen.saver import SaveLoadManager
from crygeen.settings import settings


class Direction:
    HORIZONTAL: int = 0
    VERTICAL: int = 1

    __DIR_STATUS: dict[tuple[float, float], str] = {
        (1.0, 0.0): 'right_idle', (-1.0, 0.0): 'left_idle', (0.0, 1.0): 'down_idle', (0.0, -1.0): 'up_idle',

        (0.7, 0.7): 'downright_idle', (0.7, -0.7): 'upright_idle', (-0.7, 0.7): 'downleft_idle',
        (-0.7, -0.7): 'upleft_idle',

        (0, 0): 'down_idle'
    }

    __DIR_VECTOR: dict[str, tuple[float, float]] = {
        'right': (1.0, 0.0), 'left': (-1.0, 0.0), 'down': (0.0, 1.0), 'up': (0.0, -1.0),

        'downright': (0.7, 0.7), 'upright': (0.7, -0.7), 'downleft': (-0.7, 0.7),
        'upleft': (-0.7, -0.7)
    }

    def get_direction_status(self, direction: Vector2) -> str:
        return self.__DIR_STATUS.get(
            (round(direction.x, 1), round(direction.y, 1)), (0, 0)
        )

    def get_direction_vector(self, status: str) -> tuple[float, float]:
        return self.__DIR_VECTOR.get(status, (0, 0))


class PlayerKeyboardInput:
    def __init__(self, player):  # type: ('Player') -> None
        self.player = player
        self.direction = pg.math.Vector2()
        self.control: dict[str, int] = self.get_current_control()
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
        self.attack_cd: int = 700

        self.idle = True

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
        else:
            self.keyboard_logic.idle()

    def get_current_direction(self) -> None:
        if any(self.direction.xy):
            self.current_direction: str = self.dir.get_direction_status(self.direction)

    def get_status(self) -> None:
        status: str = self.dir.get_direction_status(self.direction)
        if self.direction.xy != (0, 0):
            self.status: str = status.split('_')[0] if status else self.get_prev_dir()

    def get_prev_dir(self) -> None:
        self.prev: str = self.current_direction

    def __move(self, dt: float) -> None:
        if 'attack' not in self.status:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.player.hitbox.x += self.direction.x * self.speed * dt
            self.collision(Direction.HORIZONTAL)

            self.player.hitbox.y += self.direction.y * self.speed * dt
            self.collision(Direction.VERTICAL)

        self.player.rect.center = self.player.hitbox.center

    def collision(self, direction: int) -> None:
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

    def cooldowns(self) -> None:
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
    def get_current_control() -> dict[str, int]:
        loader: SaveLoadManager = SaveLoadManager()
        control_data: list[list[str, int, str]] = loader.load_save(settings.CONTROL_DATA_PATH)
        control: dict[str, int] = {title: constant for title, constant, _ in control_data}
        return control

    def update(self, dt: float) -> None:
        current_time = pg.time.get_ticks()
        self.get_prev_dir()  # must be first
        self.__move(dt)  # must be second
        self.get_current_direction()
        self.get_status()

        self.cooldowns()


class KeyboardLogic:
    def __init__(self, kbi: PlayerKeyboardInput) -> None:
        self.kbi: PlayerKeyboardInput = kbi

    def move_left(self) -> None:
        self.kbi.direction.x = -1

    def move_right(self) -> None:
        self.kbi.direction.x = 1

    def move_up(self) -> None:
        self.kbi.direction.y = -1

    def move_down(self) -> None:
        self.kbi.direction.y = 1

    def idle(self) -> None:
        self.kbi.idle = True
        self.kbi.direction.xy = (0, 0)
        if self.kbi.attack_available:
            self.kbi.status = self.kbi.current_direction

    def action(self):
        if self.kbi.attack_available:
            if 'attack' not in self.kbi.status:
                self.kbi.status = self.kbi.current_direction.split('_')[0] + '_attack'
            self.kbi.attack_start_time = pg.time.get_ticks()
            self.kbi.attack_available = False
            self.kbi.direction.xy = (0, 0)

    def spurt(self):
        if self.kbi.spurt_available:
            self.kbi.spurt_start_time = pg.time.get_ticks()
            self.kbi.spurt_available = False
            self.kbi.speed *= self.kbi.spurt_coefficient
