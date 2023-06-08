from typing import Any

from crygeen.game_process.animation_abc import AnimationAbc


class VargAnimation(AnimationAbc):
    def __init__(self):
        super().__init__()
        self._animation_speed: float = 5
        self._frame_index: int = 0
        self.status: str = 'up'
        self.prev_status: str = 'down_idle'

    def play_animation(self, dt: float, status: str, entity: Any, *args, **kwargs) -> None:  # noqa
        super().entity_play_animation(dt, status, entity, *args, **kwargs)

    def render(self, dt: float, status: str, entity: Any, *args, **kwargs) -> None:  # noqa
        self.play_animation(dt, status, entity, *args, **kwargs)