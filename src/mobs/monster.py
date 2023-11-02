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

    def die(self, murderer):
        if rand(1, 30) <= self.drop_rate:
            self.drop()
        if rand(1, 10) <= 1:
            self.adv_drop()
        super().die(murderer)
        self.look_normal()
        if self.map.is_visible(self.x, self.y):
            message('The %s dies!' % self.name)
        self.remove()
        murderer.kills += 1
        murderer.add_exp(self)

    def disappear(self):
        message('The %s disappears!' % self.name)
        self.remove()

    def damage(self, dmg, enemy):
        self.life.modify(-dmg)
        if self.life.cur <= 0:
            self.die(enemy)

    def drop(self):
        item = random_by_level(self.map.level, Item.ALL)()
        self.tile.items.append(item)

    def adv_drop(self):
        if self.map.player.has_life_adv_drop:
            self.tile.items.append(HealingPotion())
        if self.map.player.has_mana_adv_drop:
            self.tile.items.append(ManaPotion())

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
        mon = self.map.player
        damage = Damage.calculate(self, mon)
        mon.damage(int(damage), self)

        if damage.status == DamageStatus.NORMAL:
            message('The %s hits you (%d).' % (self.name, int(damage)))
        elif damage.status == DamageStatus.CRITICAL:
                    message('The %s critically hits you (%d)!' % (self.name, int(damage)), COLOR_ALERT)
        elif damage.status == DamageStatus.EVADED:
            message('The %s misses you.' % self.name)
        elif damage.status == DamageStatus.BLOCKED:
            message("You block the attack.")
        elif damage.status == DamageStatus.ABSORBED:
            message('Your armor protects you.')
