import tcod as T
from utils import *
from game import *
from spells import *

# --- ITEM --- #

class Item(object, metaclass=Register):
    ALL = []
    ABSTRACT = True
    common = 10

    glyph = UNKNOWN_GLYPH
    dungeons = 0, 0
    slot = None
    speed = 0
    armor = 0
    rarity = 1
    plural = False

    @property
    def descr(self):
        return self.name + self.mod_descr

    @property
    def a(self):
        if self.plural:
            return self.descr
        else:
            d = self.descr
            if d[0].lower() in 'aeiuo':
                return 'an ' + self.descr
            else:
                return 'a ' + self.descr

    @property
    def mod_descr(self):
        s = ''
        if self.speed != 0:
            s += ' (%s%d speed)' % ('+' if self.speed > 0 else '', self.speed)
        if self.armor != 0:
            s += ' (%s%d armor)' % ('+' if self.armor > 0 else '', self.armor)
        return s

    def on_equip(self, player):
        player.speed += self.speed
        player.armor += self.armor

    def on_unequip(self, player):
        player.speed -= self.speed
        player.armor -= self.armor

    def on_use(self, player):
        message('You don\'t know how to use %s.' % self.descr)

# --- LIGHT SOURCE --- #

class LightSource(Item):
    ABSTRACT = True
    slot = 'l'

    @property
    def descr(self):
        if self.turns_left == self.turns:
            s = self.name
        else:
            p = 100*self.turns_left//self.turns
            s = '%s (%s%%)' % (self.name, p)
        return s + self.mod_descr

    def __init__(self):
        super(LightSource, self).__init__()
        self.turns_left = self.turns

    def on_equip(self, player):
        player.change_light_range(self.light_range)

    def on_unequip(self, player):
        player.change_light_range(-self.light_range)

# --- WEAPON --- #

class Weapon(Item):
    ABSTRACT = True
    slot = 'w'
    common = 7

    def __init__(self):
        super(Weapon, self).__init__()
        if rand(1, 5) == 1:
            a, b, c = self.dice
            c += rand(1, 3)
            if rand(1, 9) == 1:
                b += rand(1, 2)
            self.dice = a, b, c

    @property
    def descr(self):
        return '%s (%s)%s' % (self.name, describe_dice(*self.dice), self.mod_descr)

class EliteWeapon(Weapon):
    ABSTRACT = True
    rarity = 10

class UniqueWeapon(Weapon):
    ABSTRACT = True
    rarity = 15

# --- STAFF --- #

class Staff(Weapon):
    ABSTRACT = True
    mana = 0
    magic = 1
    
    def __init__(self):
        super(Staff, self).__init__()
        if rand(1, 3) == 1:
            self.mana += rand(1, self.magic * 3)

    @property
    def mod_descr(self):    
        s = ''
        if self.mana != 0:
            s += '%s%d mana' % ('+' if self.mana > 0 else '', self.mana)
        if self.speed != 0:
            s += ', %s%d speed' % ('+' if self.speed > 0 else '', self.speed)
        if self.magic != 0:
            s += ', %s%d magic' % ('+' if self.magic > 0 else '', self.magic)
        return ' (' + s + ')'
        
    def on_equip(self, player):
        super(Staff, self).on_equip(player)
        player.max_mp += self.mana
        player.mp += self.mana
        player.magic += self.magic
    
    def on_unequip(self, player):    
        super(Staff, self).on_unequip(player)
        player.max_mp -= self.mana
        player.mp -= self.mana
        player.magic -= self.magic

class EliteStaff(Staff):
    ABSTRACT = True
    rarity = 10

class UniqueStaff(Staff):
    ABSTRACT = True
    rarity = 15

# --- ARMOR --- #

class Armor(Item):
    ABSTRACT = True

    def __init__(self):
        super(Armor, self).__init__()
        if rand(1, 5) == 1:
            self.armor = self.armor + roll(2, 2, -2)

# --- BOOTS --- #

class Boots(Armor):
    ABSTRACT = True
    slot = 'b'
    plural = True

class EliteBoots(Boots):
    ABSTRACT = True
    rarity = 10

class UniqueBoots(Boots):
    ABSTRACT = True
    rarity = 15

# --- MAIL --- #

class Mail(Armor):
    ABSTRACT = True
    slot = 'a'

# --- BOOK --- #

class Book(Item):
    ABSTRACT = True

    def on_use(self, player):
        if player.try_learn_spell(self.spell):
            player.items.remove(self)

# --- POTION --- #

class Potion(Item):
    ABSTRACT = True

    def on_use(self, player):
        message('You drink the %s.' % self.name)
        player.items.remove(self)

# --- SCROLL --- #

class Scroll(Item):
    ABSTRACT = True

    def on_use(self, player):
        if self.spell.on_use(self.spell(), player):
            player.items.remove(self)

# --- LIGHT SOURCES --- # 

class Torch(LightSource):
    name = 'torch'
    glyph = '|', T.dark_orange
    dungeons = 1, 12
    turns = 150
    light_range = 6

class Lamp(LightSource):
    name = 'lamp'
    glyph = 'o', T.dark_yellow
    dungeons = 4, 12
    rarity = 5
    turns = 300
    light_range = 8

class Lamp2(LightSource):
    name = 'lamp2'
    glyph = '0', T.light_yellow
    dungeons = 8, 12
    rarity = 15
    turns = 500
    light_range = 10

# --- DAGGERS --- #

class Dagger(Weapon):
    name = 'dagger'
    glyph = '(', T.light_grey
    speed = 1
    dice = 2, 2, 0
    dungeons = 1, 3

class Dirk(Weapon):
    name = 'dirk'
    glyph = '(', T.light_pink
    speed = 1
    dice = 2, 2, 2
    dungeons = 4, 6

class Kris(Weapon):
    name = 'kris'
    glyph = '(', T.light_green
    speed = 1
    dice = 2, 3, 4
    dungeons = 7, 9

class Rondel(Weapon):
    name = 'rondel'
    glyph = '(', T.light_blue
    speed = 1
    dice = 2, 3, 6
    dungeons = 10, 12

class BloodSpike(EliteWeapon):
    name = 'blood spike'
    glyph = '(', T.light_red
    speed = 2
    dice = 2, 4, 8
    dungeons = 7, 9

class MithrilBlade(EliteWeapon):
    name = 'mithril blade'
    glyph = '(', T.light_sky
    speed = 2
    dice = 2, 5, 10
    dungeons = 9, 11

class DivineStiletto(UniqueWeapon):
    name = 'divine stiletto'
    glyph = '(', T.light_yellow
    speed = 3
    dice = 2, 6, 12
    dungeons = 11, 12

# --- MACES --- #

class Club(Weapon):
    name = 'club'
    glyph = '/', T.dark_orange
    speed = -1
    dice = 1, 5, 0
    dungeons = 1, 3

class KillerClub(Weapon):
    name = 'killer club'
    glyph = '/', T.dark_orange
    speed = -1
    dice = 1, 5, 3
    dungeons = 4, 6

class Mace(Weapon):
    name = 'mace'
    glyph = '/', T.light_green
    dice = 2, 4, 5
    dungeons = 7, 9

class Hammer(Weapon):
    name = 'hammer'
    glyph = '/', T.light_gray
    dice = 2, 4, 9
    dungeons = 10, 12

class DeathMace(EliteWeapon):
    name = 'death mace'
    glyph = '/', T.light_gray
    dice = 2, 5, 11
    dungeons = 7, 9

class ThunderMaul(EliteWeapon):
    name = 'thunder maul'
    glyph = '/', T.blue
    dice = 2, 6, 13
    dungeons = 9, 11

class LegendaryMallet(UniqueWeapon):
    name = 'legendary mallet'
    glyph = '/', T.pink
    speed = 1
    dice = 2, 7, 15
    dungeons = 11, 12

# --- SWORDS --- #

class ShortSword(Weapon):
    name = 'short sword'
    glyph = '(', T.lighter_blue
    dice = 1, 5, 0
    dungeons = 1, 3

class Falchion(Weapon):
    name = 'falchion'
    glyph = '(', T.lighter_blue
    dice = 1, 5, 2
    dungeons = 4, 6

class BroadSword(Weapon):
    name = 'broad sword'
    glyph = '(', T.lighter_blue
    dice = 2, 5, 3
    dungeons = 7, 9

class WarSword(Weapon):
    name = 'war sword'
    glyph = '(', T.lighter_blue
    dice = 2, 6, 4
    dungeons = 10, 12

class RuneSword(EliteWeapon):
    name = 'rune sword'
    glyph = '(', T.light_gray
    dice = 2, 6, 5
    dungeons = 7, 9

class MithrilSword(EliteWeapon):
    name = 'mithril sword'
    glyph = '(', T.blue
    dice = 2, 7, 7
    dungeons = 9, 11

class AncientSword(UniqueWeapon):
    name = 'ancient sword'
    glyph = '(', T.cyan
    speed = 1
    dice = 2, 8, 11
    dungeons = 11, 12

# --- AXES --- #

class HandAxe(Weapon):
    name = 'hand axe'
    glyph = '(', T.grey
    speed = -1
    dice = 1, 4, 1
    dungeons = 1, 3

class DoubleAxe(Weapon):
    name = 'double axe'
    glyph = '(', T.grey
    dice = 1, 5, 2
    dungeons = 4, 6

class WarAxe(Weapon):
    name = 'war axe'
    glyph = '(', T.grey
    dice = 2, 5, 3
    dungeons = 7, 9

class BattleAxe(Weapon):
    name = 'battle axe'
    glyph = '(', T.grey
    dice = 2, 6, 4
    dungeons = 10, 12

class GreatAxe(EliteWeapon):
    name = 'great axe'
    glyph = '(', T.light_gray
    dice = 2, 6, 4
    dungeons = 7, 9

class GiantAxe(EliteWeapon):
    name = 'giant axe'
    glyph = '(', T.blue
    dice = 2, 6, 8
    dungeons = 9, 11

class GloriousAxe(UniqueWeapon):
    name = 'glorious axe'
    glyph = '(', T.cyan
    speed = 1
    dice = 2, 7, 14
    dungeons = 11, 12

# --- SPEARS --- #

class Spear(Weapon):
    name = 'spear'
    glyph = '/', T.light_orange
    dice = 1, 3, 1
    dungeons = 1, 3

class Pilum(Weapon):
    name = 'pilum'
    glyph = '/', T.light_orange
    dice = 1, 5, 3
    dungeons = 4, 6

class Harpoon(Weapon):
    name = 'harpoon'
    glyph = '/', T.light_orange
    dice = 2, 5, 4
    dungeons = 7, 9

class WarSpear(Weapon):
    name = 'war spear'
    glyph = '/', T.light_orange
    dice = 2, 6, 6
    dungeons = 10, 12

class GhostSpear(EliteWeapon):
    name = 'ghost spear'
    glyph = '/', T.light_grey
    speed = 1
    dice = 2, 7, 2
    dungeons = 7, 9

class MithrilMancatcher(EliteWeapon):
    name = 'mithril mancatcher'
    glyph = '/', T.light_red
    speed = 1
    dice = 2, 8, 5
    dungeons = 9, 11

class AncientPike(UniqueWeapon):
    name = 'ancient pike'
    glyph = '/', T.lighter_orange
    speed = 2
    dice = 2, 9, 10
    dungeons = 11, 12

# --- STAVES --- #

class ShortStaff(Staff):
    name = 'short staff'
    glyph = '/', T.light_orange
    speed = -1
    magic = 1
    dice = 1, 3, 1
    mana = 3
    dungeons = 1, 3

class LongStaff(Staff):
    name = 'long staff'
    glyph = '/', T.lighter_blue
    speed = -1
    magic = 2
    dice = 1, 5, 2
    mana = 6
    dungeons = 4, 6

class EmeraldStaff(Staff):
    name = 'emerald staff'
    glyph = '/', T.lighter_green
    speed = -1
    magic = 3
    dice = 2, 5, 3
    mana = 9
    dungeons = 7, 9

class SnowStaff(Staff):
    name = 'snow staff'
    glyph = '/', T.white
    speed = -1
    magic = 4
    dice = 2, 7, 4
    mana = 12
    dungeons = 10, 12

class BattleStaff(EliteStaff):
    name = 'battle staff'
    glyph = '/', T.light_grey
    magic = 5
    dice = 2, 8, 5
    mana = 14
    dungeons = 7, 9

class RuneStaff(EliteStaff):
    name = 'rune staff'
    glyph = '/', T.yellow
    magic = 6
    dice = 3, 6, 6
    mana = 17
    dungeons = 9, 11

class PowerStaff(UniqueStaff):
    name = 'power staff'
    glyph = '/', T.cyan
    speed = 1
    magic = 7
    dice = 4, 6, 5
    mana = 20
    dungeons = 11, 12

# --- BOOTS --- #

class LightBoots(Boots):
    name = 'light boots'
    glyph = '[', T.dark_orange
    armor = 1
    dungeons = 1, 3

class MeshBoots(Boots):
    name = 'mesh boots'
    glyph = '[', T.dark_red
    armor = 2
    dungeons = 4, 6

class ChainBoots(Boots):
    name = 'chain boots'
    glyph = '[', T.dark_grey
    armor = 4
    speed = -1
    dungeons = 7, 9

class HeavyBoots(Boots):
    name = 'heavy boots'
    glyph = '[', T.light_grey
    armor = 5
    speed = -2
    dungeons = 10, 12

class MirroredBoots(EliteBoots):
    name = 'mirrored boots'
    glyph = '[', T.light_green
    armor = 5
    speed = 1
    dungeons = 7, 9

class BattleBoots(EliteBoots):
    name = 'battle boots'
    glyph = '[', T.light_grey
    armor = 7
    speed = 1
    dungeons = 9, 11

class WarBoots(UniqueBoots):
    name = 'war boots'
    glyph = '[', T.light_orange
    armor = 9
    dungeons = 10, 12

class BootsOfSpeed(UniqueBoots):
    name = 'boots of speed'
    glyph = '[', T.light_blue
    armor = 3
    speed = 3
    dungeons = 10, 12

# --- ARMORS --- #

class UglyClothes(Mail):
    name = 'ugly clothes'
    plural = True
    glyph = '{', T.green
    armor = 1
    level = 1

class RingMail(Mail):
    name = 'ring mail'
    glyph = '{', T.grey
    armor = 3
    speed = -1
    level = 3
    common = 8

class PlateMail(Mail):
    name = 'plate mail'
    glyph = '{', T.cyan
    armor = 6
    speed = -2
    level = 5
    common = 6

# --- BOOKS --- #

class BookHealing(Book):
    glyph = '+', T.pink
    name = 'book of healing'
    spell = Heal
    dungeons = 1, 12
    rarity = 1
    
class BookTeleportation(Book):
    glyph = '+', T.lighter_blue
    name = 'book of teleportation'
    spell = Teleport
    dungeons = 2, 12
    rarity = 1
    
class BookBloodlust(Book):
    glyph = '+', T.red
    name = 'book of bloodlust'
    spell = Bloodlust
    dungeons = 3, 12
    rarity = 1
    
# --- POTIONS --- #

class PotionHealing(Potion):
    glyph = '!', T.light_red
    name = 'potion of healing'
    dungeons = 1, 12
    rarity = 1
    
    def on_use(self, player):
        super(PotionHealing, self).on_use(player)
        message('You feel healed.')
        player.hp = player.max_hp

class PotionOfMana(Potion):
    glyph = '!', T.light_blue
    name = 'potion of mana'
    dungeons = 1, 12
    rarity = 1
    
    def on_use(self, player):
        super(PotionOfMana, self).on_use(player)
        message('You feel magical energies restoring.')
        player.mp = player.max_mp

# --- SCROLLS --- #

class ScrollHealing(Scroll):
    glyph = '?', T.pink
    name = 'scroll of healing'
    spell = Heal
    dungeons = 1, 12
    rarity = 1

class ScrollTeleport(Scroll):
    glyph = '?', T.lighter_blue
    name = 'scroll of teleportation'
    spell = Teleport
    dungeons = 2, 12
    rarity = 1

class ScrollBloodlust(Scroll):
    glyph = '?', T.red
    name = 'scroll of bloodlust'
    spell = Bloodlust
    dungeons = 3, 12
    rarity = 1

if __name__ == '__main__':
    d = [random_by_level(1, Item.ALL)().descr for i in range(20)]
    print('\n'.join(d))
