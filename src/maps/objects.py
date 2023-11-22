import tcod as T
from common.game import *
from graphics.color import Color

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
        from graphics.scenes.final_scene import FinalScene
        from mobs.player import Invisibility
        player.invisibility = Invisibility.FULL
        message("You entered the shimmering white portal and instantly materialized in town!", T.yellow)
        prompt('Congratulations! You have won. Press [ENTER] to exit...', [pygame.K_RETURN])
        scene = FinalScene(player)
        scene.show()
        
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
    locked = False
    
    def on_enter(self):
        message('There is a %s here.' % self.name)

    def on_use(self, player, try_open = False):
        self.player = player
        if not self.used:
            if self.locked:
                if try_open and self.player.can_use_lockpick:
                    message('Opened!', Color.ALERT.value)
                    self.locked = False
                else:
                    message('Locked!', Color.ERROR.value)
                    return
            self.used = True
            message('You open a %s.' % self.name, Color.ALERT.value)
            self.on_drop(self.player)
        else:
            message('The %s is already open.' % self.name, Color.ERROR.value)

    def on_drop(self, player):
        pass
        
    def get_key(self):
        return None

    def open(self, key, player):
        if isinstance(key, self.get_key()):
            self.locked = False
            message('Opened!', Color.ALERT.value)
            self.on_use(player)
        else:
            message('Need another key!', Color.ERROR.value)

class WoodenBox(Container):
    name = "wooden box"
    glyph = "=", T.orange
    locked = False

    def on_drop(self, player):
        from mobs.drop import AdvDrop
        d = AdvDrop(player)
        d.drop()

class CopperTrunk(Container):
    name = "copper trunk"
    glyph = "=", T.copper
    locked = True

    def on_drop(self, player):
        from mobs.drop import AdvDrop
        d = AdvDrop(player)
        d.drop()

    def get_key(self):
        from items.keys import CopperKey
        return CopperKey

class SilverStrongbox(CopperTrunk):
    name = "silver strongbox"
    glyph = "=", T.silver
    container = True
    locked = True

    def on_drop(self, player):
        from mobs.drop import Drop
        super().on_drop(player)
        d = Drop(player)
        d.drop()

    def get_key(self):
        from items.keys import SilverKey
        return SilverKey

class GoldenRelicBox(SilverStrongbox):
    name = "golden relic box"
    glyph = "=", T.gold
    container = True
    locked = True
    
    def on_drop(self, player):
        from mobs.drop import RareDrop
        super().on_drop(player)
        d = RareDrop(player)
        d.drop()

    def get_key(self):
        from items.keys import GoldenKey
        return GoldenKey

class RunedChest(GoldenRelicBox):
    name = "runed chest"
    glyph = "=", T.cyan
    container = True
    locked = True

    def on_drop(self, player):
        from mobs.drop import UniqueDrop
        super().on_drop(player)
        d = UniqueDrop(player)
        d.drop()

    def get_key(self):
        from items.keys import RunedKey
        return RunedKey






















