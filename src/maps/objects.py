import tcod as T
from common.game import *

# --- MAP OBJECT --- #

class MapObject:
    name = "unknown object"
    glyph = "?", T.red
    used = False
    
    def on_enter(self):
        pass

    def on_use(self, player):
        pass

# --- PORTALS --- #

class ShimmeringRedPortal(MapObject):
    name = "shimmering red portal"
    glyph = "O", T.light_red

    def on_enter(self):
        message('There is a shimmering red portal here.')

    def on_use(self, player):
        message("You entered the shimmering red portal and found yourself in a new place!", T.yellow)
        GAME.ascend()
        

class ShimmeringGreenPortal(MapObject):
    name = "shimmering green portal"
    glyph = "O", T.light_green

    def on_enter(self):
        message('There is a shimmering green portal here.')

    def on_use(self, player):
        message("You entered the shimmering green portal and found yourself in a new place!", T.yellow)
        GAME.ascend()

class ShimmeringBluePortal(MapObject):
    name = "shimmering blue portal"
    glyph = "O", T.light_blue

    def on_enter(self):
        message('There is a shimmering blue portal here.')

    def on_use(self, player):
        message("You entered the shimmering blue portal and found yourself in a new place!", T.yellow)
        GAME.ascend()
        
class ManaShrine(MapObject):
    name = "mana shrine"
    glyph = "&", T.lighter_blue

    def on_enter(self):
        message('There is a mana shrine here.')

    def on_use(self, player):
        message('You feel magical energies restoring.')
        player.mana.fill()

class LifeShrine(MapObject):
    name = "life shrine"
    glyph = "&", T.lighter_red

    def on_enter(self):
        message('There is a life shrine here.')

    def on_use(self, player):
        message('You feel healed.')
        player.life.fill()

class RefillingShrine(MapObject):
    name = "refilling shrine"
    glyph = "&", T.lighter_green

    def on_enter(self):
        message('There is a refilling shrine here.')

    def on_use(self, player):
        message('You feel healed and magical energies restoring.')
        player.life.fill()
        player.mana.fill()

class OldTrunk(MapObject):
    name = "old trunk"
    glyph = "=", T.light_orange

    def on_enter(self):
        message('There is an old trunk here.')

    def on_use(self, player):
        from mobs.drop import AdvDrop
        if not self.used:
            self.used = True
            message('You open an old trunk.', T.yellow)
            d = AdvDrop(player)
            d.drop()
        else:
            message('The old trunk is already open.', T.red)






















