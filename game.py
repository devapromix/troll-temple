import tcod as T
from bearlibterminal import terminal as B

KEYS = []

class Game(object):
    def __init__(self, wizard):
        self.wizard = wizard
        self.scene = "game:map"

    def set_scene(self, next_scene):
        self.scene = next_scene
        
    def get_scene(self):
        return self.scene

    def play(self):
        B.open()
        B.color("white")
        
        while True:
            B.clear()
            B.puts(1, 1, "Trolls: " + self.get_scene())
            B.refresh()
            key = B.read()
            if key == B.TK_CLOSE:
                if self.scene == "menu:main":
                    break
            elif key == B.TK_ESCAPE:
                if self.scene == "menu:main":
                    break
                if self.scene == "game:map":
                    self.set_scene("menu:main")
                    continue
            elif key == B.TK_ENTER:
                pass
            key = B.read()

        B.close()

















