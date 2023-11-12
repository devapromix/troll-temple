from mobs.effects.uni_effect import UniEffect
from .game import *
from .modifiers.add_confuse import AddConfuse
from .modifiers.mod import Mod


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

class RedPortal(Spell):
    name = "red portal"
    mana = 2

    def on_use(self, player):
        f = super(RedPortal, self).on_use(player)
        if f:
            from maps.objects import ShimmeringRedPortal
            message('A shimmering red portal has opened.', COLOR_MAGIC)
            GAME.map.place_obj(player.x, player.y, ShimmeringRedPortal)
        return f

class GreenPortal(Spell):
    name = "green portal"
    mana = 2

    def on_use(self, player):
        f = super(GreenPortal, self).on_use(player)
        if f:
            from maps.objects import ShimmeringGreenPortal
            message('A shimmering green portal has opened.', COLOR_MAGIC)
            GAME.map.place_obj(player.x, player.y, ShimmeringGreenPortal)
        return f

class BluePortal(Spell):
    name = "blue portal"
    mana = 2

    def on_use(self, player):
        f = super(BluePortal, self).on_use(player)
        if f:
            from maps.objects import ShimmeringBluePortal
            message('A shimmering blue portal has opened.', COLOR_MAGIC)
            GAME.map.place_obj(player.x, player.y, ShimmeringBluePortal)
        return f

class WhitePortal(Spell):
    name = "white portal"
    mana = 2

    def on_use(self, player):
        f = super(WhitePortal, self).on_use(player)
        if f:
            from maps.objects import ShimmeringWhitePortal
            message('A shimmering white portal has opened.', COLOR_MAGIC)
            GAME.map.place_obj(player.x, player.y, ShimmeringWhitePortal)
        return f

class Heal(Spell):
    name = 'heal'
    mana = 12

    def on_use(self, player):
        f = super(Heal, self).on_use(player)
        if f:
            message('You are already at full health.', COLOR_MAGIC)
            player.life.fill()
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
            player.effects.add(UniEffect(Mod('damage_bonus', 2), player.magic + 5))
        return f
        
class Confuse(Spell):
    name = "confuse"
    mana = 20
    
    def on_use(self, player):
        f = super(Confuse, self).on_use(player)
        if f:
            mob = look_mode(True)
            if mob:
                message("The eyes of the %s look vacant..." % (mob.name), COLOR_MAGIC)
                mob.effects.add(UniEffect(AddConfuse(), player.magic + 7))
        return f











        