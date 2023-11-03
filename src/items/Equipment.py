from common.game import COLOR_MAGIC
from common.modifiers.attrib_mod import AddMaxMana
from common.modifiers.mod import Mod
from common.modifiers.modifier import Modifier
from common.utils import rand
from .Item import Item

class Equipment(Item):
    ABSTRACT = True
    magical = False
    modifier = Modifier()
    variable_mods = {'armor', 'speed', 'magic', 'mana', 'blocking', 'radius'}

    def __init__(self):
        for variable_mod in self.variable_mods:
            value = getattr(self, variable_mod, None)
            if value is not None and value != 0:
                self.modifier += Mod(variable_mod, value) if variable_mod != 'mana' else AddMaxMana(value)
    
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
