import tcod as T
from .Item import Item

class ManaOrb(Item):
    ABSTRACT = True
    glyph = 'o', T.light_blue
    name = 'mana orb'
    art = 'mana_orb'
    mana = 5
    
    def on_use(self, player):
        from common.game import message
        message('You use the %s and restored magical energy (%s).' % (self.name, self.mana))
        player.items.remove(self)
        player.mana.modify(self.mana)