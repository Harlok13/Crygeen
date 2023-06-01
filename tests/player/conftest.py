import pytest


@pytest.fixture
def create_key_mock(pressed_key):
    tmp: list = [0] * 300
    tmp[pressed_key] = 1
    return tmp


@pytest.fixture
def create_dir_status():
    return {
        (1.0, 0.0): 'right_idle', (-1.0, 0.0): 'left_idle', (0.0, 1.0): 'down_idle', (0.0, -1.0): 'up_idle',

        (0.7, 0.7): 'downright_idle', (0.7, -0.7): 'upright_idle', (-0.7, 0.7): 'downleft_idle',
        (-0.7, -0.7): 'upleft_idle',

        (0, 0): 'down_idle'
    }


@pytest.fixture
def create_dir_vector():
    return {
        'right': (1.0, 0.0), 'left': (-1.0, 0.0), 'down': (0.0, 1.0), 'up': (0.0, -1.0),

        'downright': (0.7, 0.7), 'upright': (0.7, -0.7), 'downleft': (-0.7, 0.7),
        'upleft': (-0.7, -0.7)
    }
