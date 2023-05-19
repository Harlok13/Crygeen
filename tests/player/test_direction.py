import pytest
from pygame import Vector2

from crygeen.game_process.player_setup.player_keyboard_input import Direction


class TestDirection:
    dir: Direction = Direction()

    @pytest.mark.parametrize('input_direction', [(1, 0), (0, 1), (-1, 0), (0, -1),
                                                 (0.7, 0.7), (0.7, -0.7), (-0.7, 0.7), (-0.7, -0.7),
                                                 (0, 0)])
    def test_get_direction_status(self, create_dir_status, input_direction):
        """test that get_direction_status returns the correct status"""
        self.dir.DIR_STATUS = create_dir_status
        assert self.dir.get_direction_status(Vector2(input_direction)) == self.dir.DIR_STATUS.get(input_direction)

    @pytest.mark.parametrize('input_status', [('left', 'right', 'down',  'up',
                                              'up_idle', 'down_idle', 'left_idle', 'right_idle')])
    def test_get_direction_vector(self, create_dir_vector, input_status):
        """test that get_direction_vector returns the correct vector"""
        self.dir.DIR_VECTOR = create_dir_vector
        assert self.dir.get_direction_vector(input_status) == self.dir.DIR_VECTOR.get(input_status, Vector2(0, 0))
