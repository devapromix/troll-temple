from typing import Dict

import tcod as T
from common.game import *
from common.atrib import Atrib
from mobs.effects.effects_container import EffectsContainer
from utils.event import Event
from items.corpse import Corpse


class Mob(object):
    x, y = None, None
    glyph = "?", T.red
    map = None
    enters_walls = False
    poison = 0
    poisoned = 0
    immune = False
    speed = 0
    armor = 0
    life_regen = 1
    mana_regen = 0
    blocking = 0
    accuracy = 100
    evasion = 10
    range = 1
    reflect_damage_bonus = 0
    reflect_chance_bonus = 0

    def __init__(self):
        self.life = Atrib()
        self.mana = Atrib()
        self.to_life_regen = 0
        self.to_mana_regen = 0
        self.effects = EffectsContainer(self)
        self.confused = False
        self.damage_bonus = 0
        self.on_die = Event()
        self.on_damage = Event()
        self.on_strike = Event()
        self.is_alive = True
        self.tags: Dict = dict()

    def die(self, damage):
        assert self.is_alive
        self.is_alive = False
        self.on_die(damage)
        self.tile.items.append(Corpse(self))

    def damage(self, dmg):
        self.on_damage(dmg)
        if self.is_alive:
            self.life.modify(-dmg.value)
            if self.life.cur <= 0:
                self.die(dmg)

    def attack(self, mob):
        from mobs.damage import Damage
        damage = Damage.calculate(self, mob)
        self.on_strike(damage)
        mob.damage(damage)

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
        self.effects.act()
        if self.life.cur < self.life.max:
            self.to_life_regen += self.life_regen
            if self.to_life_regen > 100:
                self.life.cur = min(self.life.max, self.to_life_regen / 100 + self.life.cur)
                self.to_life_regen %= 100
        if self.mana.cur < self.mana.max:
            self.to_mana_regen += self.mana_regen
            if self.to_mana_regen > 100:
                self.mana.cur = min(self.mana.max, self.to_mana_regen / 100 + self.mana.cur)
                self.to_mana_regen %= 100
        if self.poisoned > 0:
            if self.life.cur > 1:
                self.life.modify(-1)
            self.poisoned -= 1

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
