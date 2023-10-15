from .mob import *
from common.items import *

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