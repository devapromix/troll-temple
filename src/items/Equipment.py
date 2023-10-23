from common.game import COLOR_MAGIC
from common.utils import rand
from .item import Item

class Equipment(Item):
    ABSTRACT = True
    magical = False
    
    def suffix(self, suffix_name):
        if not self.magical:
            self.name += " of " + suffix_name
            self.color = COLOR_MAGIC
            self.magical = True
            return True
        else:
            return False
