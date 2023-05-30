import pygame as pg


class KeyboardLogic:
    def __init__(self, kbi):  # type: ('PlayerKeyboardInput') -> None
        self.kbi = kbi  # type: 'PlayerKeyboardInput'

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

            self.kbi.lightning = True

    def spurt(self):
        if self.kbi.spurt_available:
            self.kbi.spurt_start_time = pg.time.get_ticks()
            self.kbi.spurt_available = False
            self.kbi.speed *= self.kbi.spurt_coefficient
