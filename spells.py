import tcod as T
from utils import *
from game import *

# --- SPELL --- #

class Spell(object, metaclass=Register):
    ALL = []
    ABSTRACT = True

    @property
    def descr(self, player):
        return self.name + ' (mana -%d)' % (self.mana - player.game_class)
    
    def on_use(self, player):
        m = self.mana - player.game_class
        if player.mp >= m:
            message('You read the spell %s (mana -%d).' % (self.name, m))
            player.mp -= m
            return True
        else:
            message('Need more mana!')
            return False

# --- SPELLS --- #

class Heal(Spell):
    name = 'heal'
    mana = 10

    def on_use(self, player):
        f = super(Heal, self).on_use(player)
        if f:
            message('You feel healed.')
            player.hp = player.max_hp




















