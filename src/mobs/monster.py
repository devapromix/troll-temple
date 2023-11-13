from .damage import *
from .mob import *
from items.items import *

class Monster(Mob, metaclass=Register):
    ALL = []
    ABSTRACT = True
    common = 10
    multi = 1
    summoner = False
    fov_range = 5
    drop_rate = 5 # 1/30
    fears_light = False
    enters_walls = False
    dungeons = 0, 0
    rarity = 1

    def __init__(self):
        super(Monster, self).__init__()
        self.life.fill()

    def look_like(self, cls):
        self.name = cls.name
        self.glyph = cls.glyph

    def look_normal(self):
        try:
            del self.name
            del self.glyph
        except AttributeError:
            pass

    def die(self, damage):
        if rand(1, 30) <= self.drop_rate:
            self.drop()
        if rand(1, 10) <= 1:
            self.adv_drop()
        super().die(damage)
        self.look_normal()
        if self.map.is_visible(self.x, self.y):
            message('The %s dies!' % self.name)
        self.remove()
        damage.attacker.kills += 1
        damage.attacker.add_exp(self)

    def disappear(self):
        message('The %s disappears!' % self.name)
        self.remove()

    def drop(self):
        from mobs.drop import Drop
        d = Drop(self)
        d.drop()
        
    def adv_drop(self):
        from mobs.drop import AdvDrop
        d = AdvDrop(self)
        d.drop()

    def rare_drop(self):
        from mobs.drop import RareDrop
        d = RareDrop(self)
        d.drop()

    def unique_drop(self):
        from mobs.drop import UniqueDrop
        d = UniqueDrop(self)
        d.drop()

    def see_player(self):
        from mobs.player import Invisibility
        player = self.map.player
        if player.invisibility != Invisibility.NONE:
            return None
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
        super(Monster, self).act()
        player = self.map.player
        d = self.see_player()
        if d and not self.confused:
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
        self.attack(self.map.player)

    def attack(self, mob):
        damage = Damage.calculate(self, mob)
        mob.damage(damage)
