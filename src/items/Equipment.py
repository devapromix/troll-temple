from common.game import COLOR_MAGIC
from common.modifiers.modifier import Modifier
from common.utils import rand
from .Item import Item

class Equipment(Item):
    ABSTRACT = True
    magical = False
    modifier = Modifier()
    
    def suffix(self, suffix_name):
        if not self.magical:
            self.name += " of " + suffix_name
            self.color = COLOR_MAGIC
            self.magical = True
            return True
        else:
            return False

    def on_equip(self, player):
        self.modifier.commit(player)
        return True

    def on_unequip(self, player):
        self.modifier.rollback(player)

    @property
    def mod_descr(self):
        return str(self.modifier).strip()
