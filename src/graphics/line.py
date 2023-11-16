import tcod as T


class Line:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.length = 0

    def print(self, text: str, color=T.white, bkcolor=T.black):
        from common.game import out
        out(self.x + self.length, self.y, text, color, bkcolor)
        self.length += len(text)
