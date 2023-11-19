from typing import Optional, List

import pygame
import tcod as T

from .size import Size


class Window:
    __instance: Optional['Window'] = None

    def __init__(self, width: int, height: int, font: pygame.font.Font):
        self.font = font
        _txt = font.render("W", True, T.white)
        self.size: Size = Size(width, height)
        self.font_size: Size = Size(_txt.get_width(), _txt.get_height() + 1)
        self.screen = pygame.display.set_mode((self.size.Width * self.font_size.Width,
                                               self.size.Height * self.font_size.Height))
        Window.__instance = self

    def __del__(self): __instance = None

    @classmethod
    def instance(cls) -> Optional['Window']: return cls.__instance

    def set_title(self, text: str) -> None:
        pygame.display.set_caption(text)

    title = property(fset=set_title)

    def set_icon(self, path: str) -> None:
        pygame.display.set_icon(pygame.image.load(path))

    icon = property(fset=set_icon)

    def clear(self) -> None:
        self.screen.fill(T.black)

    def refresh(self) -> None:
        pygame.display.flip()

    def out(self, x, y, text, color=T.white, bkcolor=T.black, w=0) -> None:
        _txt = self.font.render(str(text), True, color, bkcolor)
        if x == 0:
            self.screen.blit(_txt, (
                int((self.size.Width - (_txt.get_width() / self.font_size.Width)) / 2) * self.font_size.Width,
                y * self.font_size.Height))
        elif w != 0:
            self.screen.blit(_txt,
                        ((x + int((w - (_txt.get_width() / self.font_size.Width)) / 2)) * self.font_size.Width,
                         y * self.font_size.Height))
        else:
            self.screen.blit(_txt, (x * self.font_size.Width, y * self.font_size.Height))


def out(x, y, text, color=T.white, bkcolor=T.black, w=0):
    Window.instance().out(x, y, text, color, bkcolor, w)


def out_list(x: int, y: int, text: List[str], color=T.white, bkcolor=T.black, w=0) -> None:
    for i, line in enumerate(text):
        out(x, y+i, line, color, bkcolor, w)


def out_text(x: int, y: int, width: int, text, color=T.white, bkcolor=T.black, w=0):
    last_space = 1
    last_drawed = -1
    line_count = 0
    for i, char in enumerate(text):
        if char == ' ':
            last_space = i
        if i - last_drawed >= width:
            out(x, y + line_count, text[last_drawed + 1: last_space], color, bkcolor)
            line_count += 1
            last_drawed = last_space

    if len(text) > last_drawed:
        out(x, y + line_count, text[last_drawed + 1:], color, bkcolor)
        line_count += 1

    return line_count


def out_file(x, y, filepath, color=T.white, bkcolor=T.black, w=0):
    with open(filepath, 'r') as f:
        for i, line in enumerate(f.readlines()):
            out(x, y + i, line.rstrip(), color, bkcolor, w)
