import tcod as T
from common.game import *

# --- MAP OBJECT --- #

class MapObject:
    name = "unknown object"
    glyph = "?", T.red
    used = False
    portal = False
    shrine = False
    container = False
    
    def on_enter(self):
        pass

    def on_use(self, player):
        pass

# --- PORTALS --- #

class ShimmeringPortal(MapObject):
    portal = True
    
    def on_use(self, player):
        GAME.ascend()

class ShimmeringRedPortal(ShimmeringPortal):
    name = "shimmering red portal"
    glyph = "O", T.light_red

    def on_enter(self):
        message('There is a shimmering red portal here.')

    def on_use(self, player):
        message("You entered the shimmering red portal and found yourself in a new place!", T.yellow)
        super().on_use(player)
        

class ShimmeringGreenPortal(ShimmeringPortal):
    name = "shimmering green portal"
    glyph = "O", T.light_green

    def on_enter(self):
        message('There is a shimmering green portal here.')

    def on_use(self, player):
        message("You entered the shimmering green portal and found yourself in a new place!", T.yellow)
        super().on_use(player)

class ShimmeringBluePortal(ShimmeringPortal):
    name = "shimmering blue portal"
    glyph = "O", T.light_blue

    def on_enter(self):
        message('There is a shimmering blue portal here.')

    def on_use(self, player):
        message("You entered the shimmering blue portal and found yourself in a new place!", T.yellow)
        super().on_use(player)
       
class ShimmeringWhitePortal(ShimmeringPortal):
    name = "shimmering white portal"
    glyph = "O", T.white

    def on_enter(self):
        message('There is a shimmering white portal here.')

    def on_use(self, player):
        message("You entered the shimmering white portal and instantly materialized in town!", T.yellow)
        self.map.player.won = True
       
class Shrine(MapObject):
    shrine = True
    
class ManaShrine(Shrine):
    name = "mana shrine"
    glyph = "&", T.lighter_blue

    def on_enter(self):
        message('There is a mana shrine here.')

    def on_use(self, player):
        if not self.used:
            self.used = True
            message('You feel magical energies restoring.')
            player.mana.fill()
        else:
            message('This mana shrine was used.', T.red)

class LifeShrine(Shrine):
    name = "life shrine"
    glyph = "&", T.lighter_red

    def on_enter(self):
        message('There is a life shrine here.')

    def on_use(self, player):
        if not self.used:
            self.used = True
            message('You feel healed.')
            player.life.fill()
        else:
            message('This life shrine was used.', T.red)

class RefillingShrine(Shrine):
    name = "refilling shrine"
    glyph = "&", T.lighter_green

    def on_enter(self):
        message('There is a refilling shrine here.')

    def on_use(self, player):
        if not self.used:
            self.used = True
            message('You feel healed and magical energies restoring.')
            player.life.fill()
            player.mana.fill()
        else:
            message('This refilling shrine was used.', T.red)

class Container(MapObject):
    container = True

class OldTrunk(Container):
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

class SilverStrongbox(OldTrunk):
    name = "silver strongbox"
    glyph = "=", T.silver
    container = True
    
    def on_enter(self):
        message('There is a silver strongbox here.')

    def on_use(self, player):
        from mobs.drop import AdvDrop, Drop
        if not self.used:
            self.used = True
            message('You open a silver strongbox.', T.yellow)
            if rand(1, 5) == 1:
                d = AdvDrop(player)
                d.drop()
            d = Drop(player)
            d.drop()
        else:
            message('The silver strongbox is already open.', T.red)

class GoldenRelicBox(SilverStrongbox):
    name = "golden relic box"
    glyph = "=", T.gold
    container = True
    
    def on_enter(self):
        message('There is a golden relic box here.')

    def on_use(self, player):
        from mobs.drop import AdvDrop, RareDrop
        if not self.used:
            self.used = True
            message('You open a silver strongbox.', T.yellow)
            d = AdvDrop(player)
            d.drop()
            r = RareDrop(player)
            r.drop()
        else:
            message('The silver strongbox is already open.', T.red)

class RunedChest(GoldenRelicBox):
    name = "runed chest"
    glyph = "=", T.cyan
    container = True
    
    def on_enter(self):
        message('There is a runed chest here.')

    def on_use(self, player):
        from mobs.drop import AdvDrop, RareDrop, UniqueDrop
        if not self.used:
            self.used = True
            message('You open a silver strongbox.', T.yellow)
            d = AdvDrop(player)
            d.drop()
            r = RareDrop(player)
            r.drop()
            u = UniqueDrop(player)
            u.drop()
        else:
            message('The silver strongbox is already open.', T.red)





















