from typing import NamedTuple

import pygame as pg


class Key(NamedTuple):
    title: str      # left
    constant: int   # pg.K_a
    key: str        # 'a'


class Control(NamedTuple):
    left: Key       # Key(pg.K_a, 'a')
    right: Key
    up: Key
    down: Key
    pause: Key
    inventory: Key
    spurt: Key
    action: Key
    slot1: Key
    slot2: Key
    slot3: Key


control = Control(

    Key('left', pg.K_a, 'a'),
    Key('right', pg.K_d, 'd'),
    Key('up', pg.K_w, 'w'),
    Key('down', pg.K_s, 's'),
    Key('pause', pg.K_ESCAPE, 'e'),
    Key('inventory', pg.K_TAB, 'TAB'),
    Key('spurt', pg.KMOD_SHIFT, 's'),
    Key('action', pg.K_SPACE, 'a'),
    Key('slot 1', pg.K_1, '1'),
    Key('slot 2', pg.K_2, '2'),
    Key('slot 3', pg.K_3, '3')

)
