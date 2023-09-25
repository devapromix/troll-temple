from bearlibterminal import terminal as B
from random import choice
import tcod as T
import utils

SCREEN_W = 100
SCREEN_H = 25

INVENTORY_SIZE = SCREEN_H - 4

MAP_W = 60 - 1
MAP_H = SCREEN_H - 1

VERSION = '0.1'

TITLE = 'Trolls v.' + VERSION

def set_color(c):
    B.color(B.color_from_argb(255, c.r, c.g, c.b))