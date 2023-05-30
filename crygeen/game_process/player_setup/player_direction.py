from pygame import Vector2


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
