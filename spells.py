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
        return str(self.name + ' (mana -%d)' % self.mana)
    
    def on_use(self, player):
        if player.mp >= self.mana:
            message('You read the spell %s (mana -%d).' % (self.name, self.mana))
            player.mp -= self.mana
            player.try_learn_spell(self)
            return True
        else:
            message('Need more mana!')
            return False

# --- SPELLS --- #

class Heal(Spell):
    name = 'heal'
    mana = 7

    def on_use(self, player):
        cast = super(Heal, self).on_use(player)
        if cast:
            message('You are already at full health.')
            player.hp = player.max_hp

class Teleport(Spell):
    name = 'teleport'
    mana = 5

    def on_use(self, player):
        cast = super(Teleport, self).on_use(player)
        if cast:
            message('You instantly materialized in another place.')
            player.teleport()





















