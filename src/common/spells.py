from mobs.effects.uni_effect import UniEffect
from .game import *
from .modifiers.add_damage import AddDamage


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
        if player.mana.cur >= self.mana:
            message('You read the spell %s (mana -%d).' % (self.name, self.mana), COLOR_MAGIC)
            player.mana.modify(-self.mana)
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
            player.effects.add(UniEffect(AddDamage(3), player.magic + 5))
        return f
        
class Confuse(Spell):
    name = "confuse"
    mana = 20
    
    def on_use(self, player):
        f = super(Confuse, self).on_use(player)
        if f:
            player.confuse_monster(player.magic + 7)
        return f











        