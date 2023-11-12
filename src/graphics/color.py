from enum import Enum
import tcod as T


class Color(Enum):
    ITEM = T.light_grey
    TITLE = T.lighter_yellow
    ALERT = T.light_yellow
    ERROR = T.lighter_red
    MAGIC = T.lighter_blue
    SELECT = T.white



