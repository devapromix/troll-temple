import pygame
import tcod as T
from common.game import out
from .point import Point


class Layout:
    def __init__(self, point: Point):
        self.point = point
        self._length = 0
        self._line_count = 0
        self.offset = 0
        self.color = T.white
        self.background_color = T.black

    @property
    def line_count(self) -> int: return self._line_count

    def print(self, text: str, color=None, background_color=None) -> None:
        x, y = self.point
        out(x + + self.offset + self._length, y + self._line_count, text,
            self.color if color is None else color,
            self.background_color if background_color is None else background_color)
        self._length += len(text)

    def next(self) -> int:
        self._line_count += 1
        self._length = 0
        return self.line_count

    def print_line(self, text: str, color=None, background_color=None) -> None:
        self.print(text, color, background_color)
        self.next()
