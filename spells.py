import tcod as T
from utils import *
from game import *

# --- SPELL --- #

class Spell(object, metaclass=Register):
    ALL = []
    ABSTRACT = True

    def __init__(self):
        pass

    @property
    def descr(self):
        return self.name + ' (mana -%d)' % self.mana
    
    def on_use(self, player):
        if player.mp >= self.mana:
            message('You read the spell %s (mana -%d).' % (self.name, self.mana))
            player.mp -= self.mana
            return True
        else:
            message('Need more mana!')
            return False

# --- SPELLS --- #

class Heal(Spell):
    name = 'heal'
    mana = 8

    def on_use(self, player):
        cast = super(Heal, self).on_use(player)
        if cast:
            message('You feel healed.')
            player.hp = player.max_hp




















