import tcod as T
from .Item import Item
from graphics.color import Color

class Key(Item):
    ABSTRACT = True
    
    def on_use(self, player):
        from common.game import message
        from maps.objects import Container
        self.player = player
        if self.player.tile.obj == None or not isinstance(self.player.tile.obj, Container):
            message('Stand on the chest to open it.', Color.ERROR.value)
            return
        self.player.tile.obj.open(self, player)

class CopperKey(Key):
    ABSTRACT = True
    glyph = '`', T.copper
    name = 'copper key'

class SilverKey(Key):
    ABSTRACT = True
    glyph = '`', T.silver
    name = 'silver key'

class GoldenKey(Key):
    ABSTRACT = True
    glyph = '`', T.gold
    name = 'golden key'

class RunedKey(Key):
    ABSTRACT = True
    glyph = '`', T.cyan
    name = 'runed key'









