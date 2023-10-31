from common.game import *

# --- MAP OBJECT --- #

class MapObject(object):
    name = "unknown object"
    glyph = UNKNOWN_GLYPH
    
    def on_enter(self, player):
        pass

# --- PORTALS --- #

class ShimmeringRedPortal(MapObject):
    name = "shimmering red portal"
    glyph = "O", T.light_red

    def on_enter(self, player):
        message("You entered the shimmering red portal and found yourself in a new place!", T.yellow)
        GAME.ascend()
        

class ShimmeringGreenPortal(MapObject):
    name = "shimmering green portal"
    glyph = "O", T.light_green

    def on_enter(self, player):
        message("You entered the shimmering green portal and found yourself in a new place!", T.yellow)
        GAME.ascend()

class ShimmeringBluePortal(MapObject):
    name = "shimmering blue portal"
    glyph = "O", T.light_blue

    def on_enter(self, player):
        message("You entered the shimmering blue portal and found yourself in a new place!", T.yellow)
        GAME.ascend()
























