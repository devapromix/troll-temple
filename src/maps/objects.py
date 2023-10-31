from common.game import *

# --- MAP OBJECT --- #

class MapObject(object):
    name = "unknown object"
    glyph = UNKNOWN_GLYPH
    
    def on_enter():
        pass

    def on_use(self, player):
        pass

# --- PORTALS --- #

class ShimmeringRedPortal(MapObject):
    name = "shimmering red portal"
    glyph = "O", T.light_red

    def on_enter():
        message('There is a shimmering red portal here.')

    def on_use(self, player):
        message("You entered the shimmering red portal and found yourself in a new place!", T.yellow)
        GAME.ascend()
        

class ShimmeringGreenPortal(MapObject):
    name = "shimmering green portal"
    glyph = "O", T.light_green

    def on_enter():
        message('There is a shimmering green portal here.')

    def on_use(self, player):
        message("You entered the shimmering green portal and found yourself in a new place!", T.yellow)
        GAME.ascend()

class ShimmeringBluePortal(MapObject):
    name = "shimmering blue portal"
    glyph = "O", T.light_blue

    def on_enter():
        message('There is a shimmering blue portal here.')

    def on_use(self, player):
        message("You entered the shimmering blue portal and found yourself in a new place!", T.yellow)
        GAME.ascend()
        
class ManaShrine(MapObject):
    name = "mana shrine"
    glyph = "*", T.lighter_blue

    def on_enter():
        message('There is a mana shrine here.')

    def on_use(self, player):
        message('You feel magical energies restoring.')
        player.mana.fill()

class LifeShrine(MapObject):
    name = "life shrine"
    glyph = "*", T.lighter_red

    def on_enter():
        message('There is a life shrine here.')

    def on_use(self, player):
        message('You feel healed.')
        player.hp = player.max_hp























