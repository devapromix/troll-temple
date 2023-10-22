from common.game import *

class Mob(object):
    x, y = None, None
    glyph = UNKNOWN_GLYPH
    map = None

    hp, max_hp = 1, 1
    mp, max_mp = 1, 1

    enters_walls = False
    poisoned = 0
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
            if self.to_hp_regen > 100:
                self.hp = min(self.max_hp, self.to_hp_regen / 100 + self.hp)
                self.to_hp_regen %= 100
        if self.mp < self.max_mp:
            self.to_mp_regen += self.mp_regen
            if self.to_mp_regen > 100:
                self.mp = min(self.max_mp, self.to_mp_regen / 100 + self.mp)
                self.to_mp_regen %= 100
        if self.poisoned > 0:
            if self.hp > 1:
                self.hp -= 1
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
