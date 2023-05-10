from typing import NamedTuple

from pygame.locals import *


class Key(NamedTuple):
    title:    str      # left
    constant: int      # pg.K_a
    key:      str      # 'a'


class Control(NamedTuple):
    left:      Key     # Key(pg.K_a, 'a')
    right:     Key
    up:        Key
    down:      Key
    pause:     Key
    inventory: Key
    spurt:     Key
    action:    Key
    slot1:     Key
    slot2:     Key
    slot3:     Key


cntrl: Control = Control(

    # title            # constant    # key
    Key('Left',        K_a,          'a'),
    Key('Right',       K_d,          'd'),
    Key('Up',          K_w,          'w'),
    Key('Down',        K_s,          's'),
    Key('Pause',       K_ESCAPE,     'esc'),
    Key('Inventory',   K_TAB,        'TAB'),
    Key('Spurt',       KMOD_SHIFT,   'shift'),
    Key('Action',      K_SPACE,      'space'),
    Key('Slot 1',      K_1,          '1'),
    Key('Slot 2',      K_2,          '2'),
    Key('Slot 3',      K_3,          '3')

)

allowed_keys: dict[int, str] = {
    K_q:               'q',
    K_w:               'w',
    K_e:               'e',
    K_r:               'r',
    K_t:               't',
    K_y:               'y',
    K_u:               'u',
    K_i:               'i',
    K_o:               'o',
    K_p:               'p',
    K_LEFTBRACKET:     '{',
    K_RIGHTBRACKET:    '}',
    K_BACKSLASH:       '\\',
    K_a:               'a',
    K_s:               's',
    K_d:               'd',
    K_f:               'f',
    K_g:               'g',
    K_h:               'h',
    K_j:               'j',
    K_k:               'k',
    K_l:               'l',
    K_SEMICOLON:       ';',
    K_QUOTE:           '\'',
    K_BACKQUOTE:       '`',
    K_z:               'z',
    K_x:               'x',
    K_c:               'c',
    K_v:               'v',
    K_b:               'b',
    K_n:               'n',
    K_m:               'm',
    K_COMMA:           ',',
    K_PERIOD:          '.',
    K_SLASH:           '/',
    K_ASTERISK:        '*',
    K_MINUS:           '-',
    K_1:               '1',
    K_2:               '2',
    K_3:               '3',
    K_4:               '4',
    K_5:               '5',
    K_6:               '6',
    K_7:               '7',
    K_8:               '8',
    K_9:               '9',
    K_0:               '0',
    K_EQUALS:          '=',
    K_F1:              'F1',
    K_F2:              'F2',
    K_F3:              'F3',
    K_F4:              'F4',
    K_F5:              'F5',
    K_F6:              'F6',
    K_F7:              'F7',
    K_F8:              'F8',
    K_F9:              'F9',
    K_F10:             'F10',
    K_F11:             'F11',
    K_F12:             'F12',
    K_LALT:            'L alt',
    K_LCTRL:           'L ctrl',
    K_RALT:            'R alt',
    K_LSHIFT:          'L shift',
    K_RSHIFT:          'R shift',
    K_SPACE:           'space',
    K_TAB:             'TAB',
    K_RETURN:          'enter',
    K_BACKSPACE:       'backspace',
    K_ESCAPE:          'esc',
    K_UP:              'up',
    K_DOWN:            'down',
    K_LEFT:            'left',
    K_RIGHT:           'right',
    K_CAPSLOCK:        'CAPS'
}

class ControlSchema(NamedTuple):
    left:      Key     # Key(pg.K_a, 'a')
    right:     Key
    up:        Key
    down:      Key
    pause:     Key
    inventory: Key
    spurt:     Key
    action:    Key
    slot1:     Key
    slot2:     Key
    slot3:     Key