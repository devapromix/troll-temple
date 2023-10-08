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
            if self.to_hp_regen > 10:
                self.hp = min(self.max_hp, self.to_hp_regen / 10 + self.hp)
                self.to_hp_regen %= 10
        if self.mp < self.max_mp:
            self.to_mp_regen += self.mp_regen
            if self.to_mp_regen > 10:
                self.mp = min(self.max_mp, self.to_mp_regen / 10 + self.mp)
                self.to_mp_regen %= 10

    def heartbeat(self):
        pass

# --- CONSTANTS --- #

FIGHTER = 1
THIEF = 2
RANGER = 3
MAGE = 4

GAME_CLASSES = [["Fighter", 1], 
                ["Thief",   2], 
                ["Ranger",  3],
                ["Mage",    4]]

# --- PLAYER --- #

class Player(Mob):
    glyph = '@', T.white
    name = 'you'
    hp_regen = 0
    mp_regen = 1
    magic = 0

    def __init__(self, wizard, selected_game_class):
        super(Player, self).__init__()
        self.game_class = selected_game_class
        self.level = 1
        self.max_hp = 40 - (self.game_class * 5)
        self.hp = self.max_hp
        self.max_mp = self.game_class * 5
        self.mp = self.max_mp

        import items as item
        import spells as spell
        self.spells = []
        self.effects = []
        self.items = [item.Torch(), item.PotionHealing()]
        if self.game_class == FIGHTER:
            self.items += [item.PotionHealing(), item.ShortSword(), item.BookHealing()]
        elif self.game_class == THIEF:
            self.items += [item.PotionHealing(), item.Dagger()]
        elif self.game_class == RANGER:
            self.items += [item.PotionHealing(), item.HandAxe()]
        else:
            self.items += [item.PotionOfMana(), item.BookHealing(), item.ShortStaff()]

        self.equipment = dict((slot, None) for slot in INVENTORY_SLOTS)
        self.speed = 0
        self.fov_range = 3
        self.light_range = 0
        self.action_turns = 1
        self.armor = 0
        self.exp = 0
        self.kills = 0
        self.deads = 0
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
        self.exp += int(1.7 ** mob.level)
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
                   T.yellow)

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

    def walk(self, dx, dy, panic=True):
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
        dmg = roll(*self.dice)
        if roll(1, 20) < 20:
            message('You hit the %s (%d).' % (mon.name, dmg))
        else:
            dmg *= 2
            message('You critically hit the %s (%d)!' % (mon.name, dmg), T.yellow)
        mon.damage(dmg)
        self.use_energy()

    def damage(self, dmg, mon):
        dmg -= self.armor
        if dmg < 0:
            message('Your armor protects you.')
            return
        self.hp -= dmg
        if self.hp <= 0:
            if not self.death:
                message('You die...', T.red)
                mon.look_normal()
                self.death = 'killed by %s' % (mon.name)

    def pick_up(self, item):
        if len(self.items) == INV_SIZE:
            message('You can\'t carry anymore items.', T.red)
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
        self.deads += 1
        self.death = None
        self.hp = self.max_hp
        self.mp = self.max_mp

    def has_spell(self, spell_type):
        for i, spell in enumerate(self.spells):
            if isinstance(spell, spell_type):
                return True
        return False
            
    def try_learn_spell(self, spell):
        if self.game_class == MAGE:
            if not self.has_spell(spell):
                self.spells.append(spell())
                message("You've learned a new spell!")
                return True
            else:
                message("You already know this spell!")
                return False
        else:
            message("You don't have a spellbook!")
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
    drop_rate = 3 # 1/30
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
        dmg -= self.armor
        if dmg < 0:
            message('The %s shrugs off the hit.' % self.name)
            return
        self.hp -= dmg
        if self.hp <= 0:
            if roll(1, 30) <= self.drop_rate:
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
            if self.summoner and roll(1, 6) == 1:
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
        player = self.map.player
        dmg = roll(*self.dice)
        if roll(1, 20) < 20:
            message('The %s hits you (%d).' % (self.name, dmg))
        else:
            dmg *= 2
            message('The %s critically hits you (%d)!' % (self.name, dmg), T.yellow)
        player.damage(dmg, self)

class UndeadMonster(Monster):
    ABSTRACT = True
    drop_rate = 0

class GhostMonster(UndeadMonster):
    ABSTRACT = True
    fears_light = True
    enters_walls = True

class MageMonster(Monster):
    ABSTRACT = True
    mp_regen = 4
    fov_range = 10
    drop_rate = 20

class BossMonster(Monster):
    ABSTRACT = True
    fov_range = 9
    drop_rate = 30

# --- MONSTERS #1 --- #

class Rat(Monster):
    name = 'rat'
    glyph = 'r', T.dark_orange
    max_hp = 4
    dice = 1, 2, 0
    drop_rate = 1
    multi = 4
    level = 1
    dungeons = 1, 2
    rarity = 1

class Bat(Monster):
    name = 'bat'
    glyph = 'b', T.darker_orange
    max_hp = 5
    speed = 3
    dice = 1, 3, 0
    multi = 3
    fears_light = True
    level = 1
    dungeons = 1, 4
    rarity = 1

# --- MONSTERS #2 --- #

class GiantSpider(Monster):
    name = 'giant spider'
    glyph = 's', T.light_gray
    max_hp = 7
    speed = 1
    dice = 1, 4, 0
    armor = 0
    multi = 3
    level = 2
    dungeons = 2, 3
    rarity = 1

class Kobold(Monster):
    name = 'kobold'
    glyph = 'k', T.light_green
    max_hp = 10
    dice = 1, 4, 1
    speed = 1
    armor = 0
    multi = 3
    level = 2
    dungeons = 2, 3
    rarity = 1

# --- MONSTERS #3 --- #

class Goblin(Monster):
    name = 'goblin'
    glyph = 'g', T.light_blue
    max_hp = 15
    dice = 1, 5, 1
    armor = 1
    level = 3
    dungeons = 3, 4
    rarity = 1

# --- MONSTERS #4 --- #

class Orc(Monster):
    name = 'orc'
    glyph = 'o', T.red
    max_hp = 20
    dice = 2, 3, 1
    armor = 3
    level = 4
    dungeons = 4, 5
    rarity = 1

# --- MONSTERS #5 --- #

class Ghost(GhostMonster):
    name = 'ghost'
    glyph = 'g', T.white
    max_hp = 26
    speed = 2
    dice = 2, 4, 1
    level = 5    
    multi = 3
    dungeons = 5, 6
    rarity = 1

class KillerBat(Monster):
    name = 'killer bat'
    glyph = 'b', T.darker_orange
    max_hp = 20
    speed = 4
    dice = 3, 3, 0
    multi = 3
    fears_light = True
    level = 1
    dungeons = 5, 7
    rarity = 1

# --- MONSTERS #6 --- #

class Troll(Monster):
    name = 'troll'
    glyph = 'T', T.blue
    max_hp = 32
    dice = 2, 6, 2
    level = 6    
    dungeons = 6, 7
    rarity = 1

# --- MONSTERS #7 --- #

class Ogre(Monster):
    name = 'ogre'
    glyph = 'O', T.light_green
    max_hp = 40
    dice = 2, 8, 3
    level = 7    
    dungeons = 7, 8
    rarity = 1

# --- MONSTERS #8 --- #

class Skeleton(UndeadMonster):
    name = 'skeleton'
    glyph = 's', T.light_grey
    max_hp = 35
    dice = 2, 6, 0
    level = 8    
    dungeons = 8, 8
    rarity = 1

class Zombie(UndeadMonster):
    name = 'zombie'
    glyph = 'z', T.light_green
    max_hp = 38
    dice = 2, 7, 0
    level = 8    
    dungeons = 8, 8
    rarity = 1

class BoneGolem(UndeadMonster):
    name = 'bone golen'
    glyph = 'G', T.light_grey
    max_hp = 45
    dice = 3, 6, 0
    level = 8    
    dungeons = 8, 8
    rarity = 15

class Necromancer(MageMonster):
    name = 'necromancer'
    glyph = 'N', T.light_grey
    max_hp = 25
    dice = 3, 5, 2
    summoner = True
    level = 8    
    dungeons = 8, 8
    rarity = 5

# --- MONSTERS #9 --- #

class Golem(Monster):
    name = 'golem'
    glyph = 'G', T.light_grey
    max_hp = 45
    dice = 3, 6, 3
    level = 9    
    dungeons = 9, 10
    rarity = 1

# --- MONSTERS #10 --- #

class Wraith(GhostMonster):
    name = 'wraith'
    glyph = 'w', T.light_grey
    max_hp = 47
    dice = 3, 7, 4
    level = 10    
    dungeons = 10, 11
    rarity = 1

# --- MONSTERS #11 --- #

class Spectre(GhostMonster):
    name = 'spectre'
    glyph = 's', T.light_grey
    max_hp = 50
    speed = 1
    dice = 3, 8, 3
    multi = 3
    level = 11    
    dungeons = 11, 12
    rarity = 1

# --- MONSTERS #12 --- #

class Summoner(MageMonster):
    name = 'summoner'
    glyph = 'S', T.light_blue
    max_hp = 45
    dice = 3, 8, 5
    summoner = True
    multi = 3
    level = 12    
    dungeons = 12, 12
    rarity = 5

# --- BOSS --- #

class TrollKing(BossMonster):
    ABSTRACT = True
    name = 'Troll King'
    glyph = 'T', T.red
    max_hp = 75
    dice = 4, 7, 10
    armor = 10
    level = 12
    dungeons = 12, 12

    def die(self):
        super(TrollKing, self).die()
        self.map.player.won = True
        
if __name__ == '__main__':
    d = [random_by_level(1, Monster.ALL)().name for i in range(20)]
    print('\n'.join(d))
