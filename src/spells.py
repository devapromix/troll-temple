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
            message('You read the spell %s (mana -%d).' % (self.name, self.mana), COLOR_MAGIC)
            player.mp -= self.mana
            return True
        else:
            message('Need more mana!', COLOR_ERROR)
            return False

# --- SPELLS --- #

class Heal(Spell):
    name = 'heal'
    mana = 12

    def on_use(self, player):
        f = super(Heal, self).on_use(player)
        if f:
            message('You are already at full health.', COLOR_MAGIC)
            player.hp = player.max_hp
        return f

class Teleport(Spell):
    name = 'teleport'
    mana = 15

    def on_use(self, player):
        f = super(Teleport, self).on_use(player)
        if f:
            message('You instantly materialized in another place.', COLOR_MAGIC)
            player.teleport()
        return f

class Bloodlust(Spell):
    name = 'bloodlust'
    mana = 18

    def on_use(self, player):
        f = super(Bloodlust, self).on_use(player)
        if f:
            message('You feel lust for blood.', COLOR_MAGIC)
            player.add_effect("bloodlust", 5)
        return f




















