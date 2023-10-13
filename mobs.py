from math import log
import tcod as T
from utils import *
from items import *
from game import *

# --- MOB --- #

class Mob(object):
    x, y = None, None
    glyph = UNKNOWN_GLYPH
    map = None

    hp, max_hp = 1, 1
    mp, max_mp = 1, 1

    enters_walls = False
    speed = 0
    armor = 0
    hp_regen = 1
    mp_regen = 0

    def __init__(self):
        self.to_hp_regen = 0
        self.to_mp_regen = 0

    @property
    def tile(self):
        return self.map.tiles[self.x][self.y]

    def put(self, m, x, y):
        tile = m.tiles[x][y]
        self.map = m
        self.x, self.y = x, y
        assert self.tile.mob is None
        self.tile.mob = self
        m.mobs.append(self)

    def remove(self):
        self.tile.mob = None
        self.map.mobs.remove(self)

    def move(self, x, y):
        self.tile.mob = None
        self.x, self.y = x, y
        assert self.tile.mob is None
        self.tile.mob = self

    def can_walk(self, dx, dy):
        destx, desty = self.x + dx, self.y + dy
        if not self.map.in_map(destx, desty):
            return False
        tile = self.map.tiles[destx][desty]
        return (tile.walkable or self.enters_walls) and \
            not tile.mob

    def walk(self, dx, dy):
        self.move(self.x + dx, self.y + dy)

    def is_besides(self, mob):
        return max(abs(self.x - mob.x), abs(self.y - mob.y)) == 1

    def act(self):
        if self.hp < self.max_hp:
            self.to_hp_regen += self.hp_regen
            if self.to_hp_regen > 50:
                self.hp = min(self.max_hp, self.to_hp_regen / 50 + self.hp)
                self.to_hp_regen %= 50
        if self.mp < self.max_mp:
            self.to_mp_regen += self.mp_regen
            if self.to_mp_regen > 50:
                self.mp = min(self.max_mp, self.to_mp_regen / 50 + self.mp)
                self.to_mp_regen %= 50

    def heartbeat(self):
        pass
    
    def calc_damage(self, dmg):
        if dmg < 1:
            dmg = 1
        if self.armor > 90:
            self.armor = 90
        if self.armor < 0:
            self.armor = 0
            return dmg
        return round(dmg * (100 - self.armor) / 100)

# --- CONSTANTS --- #

FIGHTER = 1
THIEF = 2
RANGER = 3
MAGE = 4

GAME_CLASSES = [["Fighter", 1, T.light_red], 
                ["Thief",   2, T.light_yellow], 
                ["Ranger",  3, T.light_green],
                ["Mage",    4, T.light_orange]]

# --- PLAYER --- #

class Player(Mob):
    glyph = '@', T.white
    name = 'you'
    hp_regen = 0
    mp_regen = 1
    magic = 0
    radius = 0

    def __init__(self, wizard, selected_game_class):
        super(Player, self).__init__()
        self.game_class = selected_game_class
        self.level = 1
        self.max_hp = 40 - (self.game_class * 5)
        self.hp = self.max_hp
        self.max_mp = self.game_class * 5
        self.mp = self.max_mp
        self.has_spellbook = False
        self.has_craftbox = False
        self.has_alchemyset = False

        import items as item
        import spells as spell
        self.spells = []
        self.effects = []
        self.items = [item.Torch(), item.PotionHealing()]
        if self.game_class == FIGHTER:
            self.hp_regen = 2
            self.mp_regen = 0
            self.magic = 0
            self.radius = 0
            self.items += [item.PotionHealing(), item.ShortSword()]
        elif self.game_class == THIEF:
            self.hp_regen = 1
            self.mp_regen = 1
            self.magic = 0
            self.radius = 0
            self.has_alchemyset = True
            self.items += [item.PotionHealing(), item.Dagger()]
        elif self.game_class == RANGER:
            self.hp_regen = 1
            self.mp_regen = 1
            self.magic = 0
            self.radius = 1
            self.has_craftbox = True
            self.items += [item.PotionHealing(), item.Spear()]
        else:
            self.hp_regen = 0
            self.mp_regen = 2
            self.magic = 1
            self.radius = 0
            self.has_spellbook = True
            self.items += [item.PotionOfMana(), item.BookHealing(), item.ShortStaff()]

        self.equipment = dict((slot, None) for slot in INVENTORY_SLOTS)
        self.speed = 0
        self.fov_range = 3
        self.light_range = 0
        self.action_turns = 1
        self.armor = 0
        self.exp = 0
        self.kills = 0
        self.deaths = 0
        self.death = None
        self.won = False
        self.wizard = wizard

    @property
    def dice(self):
        weapon = self.equipment['w']
        if weapon:
            a, b, c = weapon.dice
        else:
            a, b, c = 1, 3, 0
        return a, b, c

    def max_exp(self):
        return (self.level * 9) + ((self.level - 1) * self.level)

    def add_exp(self, mob):
        self.exp += mob.level
        if self.exp >= self.max_exp():
            self.exp -= self.max_exp()
            self.advance()

    def hp_inc(self):
        if self.game_class == FIGHTER:
            return 4
        elif self.game_class == THIEF:
            return 3
        elif self.game_class == RANGER:
            return 3
        else:
            return 2

    def mp_inc(self):
        if self.game_class == FIGHTER:
            return 1
        elif self.game_class == THIEF:
            return 2
        elif self.game_class == RANGER:
            return 2
        else:
            return 5

    def advance(self):
        self.level += 1
        self.max_hp += self.hp_inc()
        self.hp = self.max_hp
        self.max_mp += self.mp_inc()
        self.mp = self.max_mp

        message('Congratulations! You advance to level %d.' % self.level,
                   COLOR_ALERT)

    def change_light_range(self, n):
        self.light_range += n
        self.fov_range += n
        self.map.recalc_fov()

    def has_equipped(self, item):
        return item.slot and self.equipment[item.slot] == item

    def put(self, m, x, y):
        super(Player, self).put(m, x, y)
        self.map.player = self
        self.map.recalc_fov()

    def move(self, x, y):
        super(Player, self).move(x, y)
        self.map.recalc_fov()
        self.tile.on_enter()
        if self.tile.items:
            if len(self.tile.items) == 1:
                message('You see here %s.' % self.tile.items[0].a)
            else:
                message('Several items are lying here.')
        self.use_energy()

    def walk(self, dx, dy):
        destx, desty = self.x+dx, self.y+dy
        if not self.map.in_map(destx, desty):
            return False
        tile = self.map.tiles[destx][desty]
        if tile.mob:
            self.attack(tile.mob)
        elif not tile.walkable and not self.wizard:
            pass
        else:
            self.move(destx, desty)

    def use(self, item):
        if item.slot is None:
            item.on_use(self)
            self.use_energy()
        elif self.has_equipped(item):
            self.unequip(item)
        else:
            self.equip(item)
            
    def use_spell(self, spell):
        if spell.on_use(self):
            self.use_energy()

    def unequip(self, item):
        message('You unequip the %s.' % item.descr)
        item.on_unequip(self)
        self.equipment[item.slot] = None
        self.use_energy()

    def equip(self, item):
        old_item = self.equipment[item.slot]
        if old_item:
            self.unequip(old_item)
        message('You equip the %s.' % item.descr)
        item.on_equip(self)
        self.equipment[item.slot] = item
        self.use_energy()

    def attack(self, mon):
        if rand(1, 100) < 95:
            dmg = roll(*self.dice)
            dmg = mon.calc_damage(dmg)
            if dmg > 0:
                if rand(1, 20) < 20:
                    message('You hit the %s (%d).' % (mon.name, dmg))
                else:
                    dmg *= 2
                    message('You critically hit the %s (%d)!' % (mon.name, dmg), COLOR_ALERT)
            mon.damage(dmg)
            self.use_energy()
        else:
            message('You miss the %s.' % (mon.name))

    def damage(self, dmg, mon):
        if dmg <= 0:
            message('Your armor protects you.')
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            if not self.death:
                message('You die...', COLOR_ERROR)
                mon.look_normal()
                self.death = 'killed by %s' % (mon.name)

    def pick_up(self, item):
        if len(self.items) == INV_SIZE:
            message('You can\'t carry anymore items.', COLOR_ERROR)
            return
        assert item in self.tile.items
        self.tile.items.remove(item)
        self.items.append(item)
        message('You pick up the %s.' % item.descr)
        self.use_energy()

    def drop(self, item):
        if self.has_equipped(item):
            self.unequip(item)
        self.items.remove(item)
        self.tile.items.append(item)
        message('You drop the %s.' % item.descr)
        self.use_energy()

    def act(self):
        if not self.death:
            super(Player, self).act()
        self.action_turns += 1
        self.act_effects()

    def use_energy(self):
        self.action_turns -= 1

    def wait(self):
        self.use_energy()

    def extinguish(self, light):
        message('Your %s is extinguished!' % light.descr)
        light.on_unequip(self)
        self.equipment['l'] = None
        self.items.remove(light)

    def heartbeat(self):
        super(Player, self).heartbeat()
        light = self.equipment['l']
        if light:
            light.turns_left -= 1
            if light.turns_left <= 0:
                self.extinguish(light)

    def resurrect(self):
        self.deaths += 1
        self.death = None
        self.hp = self.max_hp
        self.mp = self.max_mp

    def has_spell(self, spell_type):
        for i, spell in enumerate(self.spells):
            if isinstance(spell, spell_type):
                return True
        return False
            
    def try_learn_spell(self, spell):
        if self.has_spellbook:
            if not self.has_spell(spell):
                self.spells.append(spell())
                message("You've learned a new spell!", COLOR_MAGIC)
                return True
            else:
                message("You already know this spell!", COLOR_ERROR)
                return False
        else:
            message("You don't have a spellbook!", COLOR_ERROR)
            return False
            
    def heal(self, hp):
        self.hp += hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp
            
    def teleport(self):
        x, y, _ = self.map.random_empty_tile()
        self.move(x, y)
 
    def has_effect(self, effect):
        for i, ef in enumerate(self.effects):
            if ef[0] == effect:
                return True
        return False
 
    def add_effect(self, effect, turns):
        if not self.has_effect(effect):
            self.effects.append([effect, turns])
        print(self.effects)
 
    def act_effects(self):
        pass
 
 
 # --- MONSTER --- #

class Monster(Mob, metaclass=Register):
    ALL = []
    ABSTRACT = True
    multi = 1
    common = 10
    summoner = False
    fov_range = 5
    drop_rate = 5 # 1/30
    fears_light = False
    enters_walls = False
    dungeons = 0, 0
    rarity = 1

    def __init__(self):
        super(Monster, self).__init__()
        self.hp = self.max_hp

    def look_like(self, cls):
        self.name = cls.name
        self.glyph = cls.glyph

    def look_normal(self):
        try:
            del self.name
            del self.glyph
        except AttributeError:
            pass

    def disappear(self):
        message('The %s disappears!' % self.name)
        self.remove()

    def damage(self, dmg):
        if dmg <= 0:
            message('The %s shrugs off the hit.' % self.name)
            return
        self.hp -= dmg
        if self.hp <= 0:
            if rand(1, 30) <= self.drop_rate:
                item = random_by_level(self.map.level, Item.ALL)()
                self.tile.items.append(item)
            self.die()
        else:
            message('The %s is %s.' % (self.name, self.get_wounds()))

    def die(self):
        self.look_normal()
        if self.map.is_visible(self.x, self.y):
            message('The %s dies!' % self.name)
        self.remove()
        self.map.player.kills += 1
        self.map.player.add_exp(self)

    def get_wounds(self):
        p = 100*self.hp/self.max_hp
        if p < 10:
            return 'almost dead'
        elif p < 30:
            return 'severely wounded'
        elif p < 70:
            return 'moderately wounded'
        else:
            return 'lightly wounded'

    def see_player(self):
        player = self.map.player
        fov_range = self.fov_range + player.light_range/2
        if T.map_is_in_fov(self.map.fov_map, self.x, self.y):
            d = dist(self.x, self.y, player.x, player.y)
            if d <= fov_range:
                return d
        return None

    def walk_randomly(self):
        dirs = [dx_dy for dx_dy in ALL_DIRS if self.can_walk(dx_dy[0], dx_dy[1])]
        if dirs != []:
            self.walk(*choice(dirs))

    def summon_monsters(self):
        if self.map.is_visible(self.x, self.y):
            message('The %s summons monsters!' % self.name)
        else:
            message('You hear arcane mumbling.')
        n = roll(2, 3)
        mcls = random_by_level(self.map.level, Monster.ALL)
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        shuffle(dirs)
        for dx, dy in dirs:
            n = self.map.flood(self.x+dx, self.y+dy, mcls, n)

    def act(self):
        player = self.map.player
        d = self.see_player()
        if d:
            if self.summoner and rand(1, 6) == 1:
                self.summon_monsters()
                return
            dx, dy = dir_towards(self.x, self.y,
                                 player.x, player.y)
            if player.light_range > 0 and self.fears_light:
                if self.can_walk(-dx, -dy):
                    self.walk(-dx, -dy)
                elif player.is_besides(self):
                    self.attack_player()
                else:
                    self.walk_randomly()
            else:
                if player.is_besides(self):
                    self.attack_player()
                elif self.can_walk(dx, dy):
                    self.walk(dx, dy)
                else:
                    self.walk_randomly()
        else:
            self.walk_randomly()

    def attack_player(self):
        if rand(1, 100) < 95:
            player = self.map.player
            dmg = roll(*self.dice)
            dmg = player.calc_damage(dmg)
            if dmg > 0:
                if rand(1, 20) < 20:
                    message('The %s hits you (%d).' % (self.name, dmg))
                else:
                    dmg *= 2
                    message('The %s critically hits you (%d)!' % (self.name, dmg), COLOR_ALERT)
            player.damage(dmg, self)
        else:
            message('The %s misses you.' % (self.name))

class FlyMonster(Monster):
    ABSTRACT = True
    fears_light = True
    drop_rate = 10

class UndeadMonster(Monster):
    ABSTRACT = True
    drop_rate = 10

class GhostMonster(UndeadMonster):
    ABSTRACT = True
    fears_light = True
    enters_walls = True
    drop_rate = 10

class MageMonster(Monster):
    ABSTRACT = True
    mp_regen = 10
    fov_range = 10
    drop_rate = 20

class RareMonster(Monster):
    ABSTRACT = True
    hp_regen = 5
    drop_rate = 30
    rarity = 15

class BossMonster(Monster):
    ABSTRACT = True
    hp_regen = 5
    fov_range = 7
    drop_rate = 30

class FinalBossMonster(BossMonster):
    ABSTRACT = True
    hp_regen = 10
    fov_range = 10
    drop_rate = 30

# --- MONSTERS #1 --- #

class Rat(Monster):
    name = 'rat'
    glyph = 'r', T.light_gray
    max_hp = 4
    dice = 1, 2, 0
    multi = 4
    level = 1
    dungeons = 1, 2
    rarity = 1

class Bat(FlyMonster):
    name = 'bat'
    glyph = 'b', T.darker_orange
    max_hp = 6
    speed = 3
    dice = 1, 2, 0
    multi = 3
    level = 1
    dungeons = 1, 3
    rarity = 1

class Crawler(Monster):
    name = 'crawler'
    glyph = 'c', T.light_blue
    max_hp = 5
    dice = 1, 2, 0
    multi = 3
    level = 1
    dungeons = 1, 2
    rarity = 1

# --- MONSTERS #2 --- #

class GiantSpider(Monster):
    name = 'giant spider'
    glyph = 's', T.light_gray
    max_hp = 8
    speed = 1
    dice = 1, 3, 0
    armor = 0
    multi = 3
    level = 2
    dungeons = 2, 3
    rarity = 1

class Kobold(Monster):
    name = 'kobold'
    glyph = 'k', T.light_green
    max_hp = 10
    dice = 1, 3, 1
    speed = 1
    armor = 0
    multi = 3
    level = 2
    dungeons = 2, 3
    rarity = 1

class Lizard(Monster):
    name = 'lizard'
    glyph = 'l', T.light_blue
    max_hp = 9
    dice = 1, 3, 0
    armor = 1
    multi = 3
    level = 2
    dungeons = 2, 3
    rarity = 1

# --- MONSTERS #3 --- #

class BlackKobold(Monster):
    name = 'black kobold'
    glyph = 'k', T.gray
    max_hp = 12
    dice = 1, 3, 1
    armor = 0
    level = 3
    dungeons = 3, 4
    rarity = 1

class Bloodfly(Monster):
    name = 'bloodfly'
    glyph = 'b', T.gray
    max_hp = 16
    dice = 1, 3, 0
    armor = 1
    level = 3
    dungeons = 3, 4
    rarity = 1

class Goblin(Monster):
    name = 'goblin'
    glyph = 'g', T.light_blue
    max_hp = 14
    dice = 1, 3, 2
    armor = 1
    level = 3
    dungeons = 3, 4
    rarity = 1

# --- MONSTERS #4 --- #

class DarkGoblin(Monster):
    name = 'dark goblin'
    glyph = 'g', T.grey
    max_hp = 18
    dice = 2, 3, 0
    armor = 1
    level = 4
    dungeons = 4, 5
    rarity = 1

class LowOrc(Monster):
    name = 'low orc'
    glyph = 'o', T.red
    max_hp = 20
    dice = 2, 3, 1
    armor = 2
    level = 4
    dungeons = 4, 5
    rarity = 1

class CrystalSpider(Monster):
    name = 'crystal spider'
    glyph = 's', T.light_cyan
    max_hp = 19
    dice = 2, 3, 1
    armor = 1
    level = 4
    multi = 2
    dungeons = 4, 5
    rarity = 1

# --- MONSTERS #5 --- #

class Scavenger(GhostMonster):
    name = 'scavenger'
    glyph = 's', T.light_green
    max_hp = 25
    dice = 2, 3, 2
    level = 5    
    armor = 2
    dungeons = 5, 6
    rarity = 1

class Ghost(GhostMonster):
    name = 'ghost'
    glyph = 'g', T.white
    max_hp = 24
    speed = 1
    dice = 2, 4, 0
    level = 5    
    multi = 2
    dungeons = 5, 6
    rarity = 1

class KillerBat(FlyMonster):
    name = 'killer bat'
    glyph = 'b', T.darker_orange
    max_hp = 22
    speed = 3
    dice = 3, 3, 0
    multi = 3
    level = 5
    dungeons = 5, 7
    rarity = 1

# --- MONSTERS #6 --- #

class RockRat(Monster):
    name = 'rock rat'
    glyph = 'r', T.light_gray
    max_hp = 28
    dice = 2, 5, 0
    multi = 3
    level = 6
    dungeons = 6, 8
    rarity = 1

class Snapper(Monster):
    name = 'snapper'
    glyph = 's', T.lighter_green
    max_hp = 32
    dice = 2, 4, 1
    level = 6
    dungeons = 6, 8
    rarity = 1

class Troll(RareMonster):
    name = 'troll'
    glyph = 'T', T.light_blue
    max_hp = 30
    dice = 2, 5, 2
    level = 6    
    armor = 5
    dungeons = 6, 7

# --- MONSTERS #7 --- #

class FlyingEye(FlyMonster):
    name = 'flying eye'
    glyph = 'e', T.light_blue
    max_hp = 32
    dice = 2, 5, 0
    multi = 3
    level = 7
    dungeons = 7, 7
    rarity = 1

class FireSkeleton(UndeadMonster):
    name = 'fire skeleton'
    glyph = 's', T.light_red
    max_hp = 35
    dice = 2, 5, 2
    multi = 2
    level = 7
    dungeons = 7, 8
    rarity = 1

class StoneShark(Monster):
    name = 'stoneshark'
    glyph = 's', T.light_grey
    max_hp = 35
    dice = 2, 6, 0
    armor = 2
    level = 7
    dungeons = 7, 8
    rarity = 1

class Ogre(RareMonster):
    name = 'ogre'
    glyph = 'O', T.light_green
    max_hp = 36
    dice = 2, 6, 2
    armor = 7
    level = 7    
    dungeons = 7, 8

# --- MONSTERS #8 --- #

class Skeleton(UndeadMonster):
    name = 'skeleton'
    glyph = 's', T.light_grey
    max_hp = 37
    dice = 2, 5, 3
    multi = 2
    level = 8    
    dungeons = 8, 8
    rarity = 1

class Zombie(UndeadMonster):
    name = 'zombie'
    glyph = 'z', T.light_green
    max_hp = 38
    dice = 2, 6, 1
    level = 8    
    dungeons = 8, 8
    rarity = 1

class BoneGolem(UndeadMonster):
    name = 'bone golem'
    glyph = 'G', T.light_grey
    max_hp = 42
    armor = 7
    dice = 3, 4, 3
    level = 8    
    dungeons = 8, 9
    rarity = 15

class Necromancer(MageMonster):
    name = 'necromancer'
    glyph = 'n', T.light_grey
    max_hp = 40
    dice = 3, 4, 2
    summoner = True
    level = 8    
    dungeons = 8, 8
    rarity = 5

# --- MONSTERS #9 --- #

class MaddeningEye(FlyMonster):
    name = 'maddening eye'
    glyph = 'e', T.yellow
    max_hp = 44
    dice = 3, 5, 0
    armor = 1
    level = 9    
    dungeons = 9, 10
    rarity = 1

class Shadowbeast(UndeadMonster):
    name = 'shadowbeast'
    glyph = 's', T.light_grey
    max_hp = 44
    dice = 2, 5, 5
    armor = 2
    level = 9    
    dungeons = 8, 10
    rarity = 1

class StoneGolem(RareMonster):
    name = 'stone golem'
    glyph = 'G', T.light_grey
    max_hp = 44
    armor = 10
    dice = 3, 5, 2
    level = 9    
    dungeons = 9, 10

class FireGolem(RareMonster):
    name = 'fire golem'
    glyph = 'G', T.light_red
    max_hp = 46
    armor = 10
    dice = 3, 5, 2
    level = 9    
    dungeons = 9, 10

# --- MONSTERS #10 --- #

class RockRaider(Monster):
    name = 'rock raider'
    glyph = 'r', T.light_grey
    max_hp = 48
    armor = 4
    dice = 2, 7, 2
    level = 10    
    dungeons = 10, 11
    rarity = 1

class DustDevil(Monster):
    name = 'dust devil'
    glyph = 'd', T.yellow
    max_hp = 52
    dice = 2, 8, 1
    armor = 7
    level = 10    
    dungeons = 10, 11
    rarity = 1

class Wraith(GhostMonster):
    name = 'wraith'
    glyph = 'w', T.light_grey
    max_hp = 50
    dice = 3, 5, 2
    level = 10    
    dungeons = 10, 11
    rarity = 1

# --- MONSTERS #11 --- #

class Drake(Monster):
    name = 'drake'
    glyph = 'd', T.light_green
    max_hp = 55
    dice = 2, 9, 0
    armor = 3
    level = 11    
    dungeons = 11, 12
    rarity = 1

class Spectre(GhostMonster):
    name = 'spectre'
    glyph = 's', T.light_grey
    max_hp = 54
    speed = 1
    dice = 3, 6, 0
    multi = 3
    level = 11    
    dungeons = 11, 12
    rarity = 1

class Wyrm(Monster):
    name = 'wyrm'
    glyph = 'w', T.light_grey
    max_hp = 56
    dice = 3, 6, 1
    armor = 5
    level = 11    
    dungeons = 11, 12
    rarity = 1

class ColossalHydra(RareMonster):
    name = 'colossal hydra'
    glyph = 'H', T.dark_green
    max_hp = 58
    armor = 12
    dice = 4, 4, 4
    level = 11    
    dungeons = 11, 12

# --- MONSTERS #12 --- #

class SoulSucker(FlyMonster):
    name = 'soul sucker'
    glyph = 's', T.light_blue
    max_hp = 60
    dice = 3, 7, 0
    armor = 4
    multi = 3
    level = 12    
    dungeons = 12, 12
    rarity = 1

class HugeSpider(Monster):
    name = 'huge spider'
    glyph = 's', T.light_red
    max_hp = 60
    dice = 3, 6, 3
    armor = 8
    level = 12    
    dungeons = 12, 12
    rarity = 1

class Summoner(MageMonster):
    name = 'summoner'
    glyph = 's', T.light_blue
    max_hp = 60
    dice = 3, 6, 2
    summoner = True
    multi = 3
    armor = 5
    level = 12    
    dungeons = 12, 12
    rarity = 5

# --- BOSS --- #

class TrollKing(FinalBossMonster):
    ABSTRACT = True
    name = 'Troll King'
    glyph = 'T', T.red
    max_hp = 75
    dice = 4, 6, 5
    armor = 10
    level = 12
    dungeons = 12, 12

    def die(self):
        super(TrollKing, self).die()
        self.map.player.won = True
        
if __name__ == '__main__':
    d = [random_by_level(1, Monster.ALL)().name for i in range(20)]
    print('\n'.join(d))
