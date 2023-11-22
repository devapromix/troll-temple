from mobs.mobs import *
from items.items import *
from maps.objects import *

class Map(object):
    def __init__(self, level):
        from maps.generator import MapGenerator
        self.generator = MapGenerator()
        self.tiles = self.generator.generate(level)
        self.level = level

        self.player = None
        self.mobs = []

        self.fov_map = T.map_new(MAP_W, MAP_H)
        for x in range(MAP_W):
            for y in range(MAP_H):
                tile = self.tiles[x][y]
                T.map_set_properties(self.fov_map,
                                           x, y,
                                           tile.transparent,
                                           tile.walkable)

        self.populate()
        
        if self.level == 3:
            self.place_monsters(FireGoblin)
        elif self.level == 6:
            self.place_monsters(Werewolf)
        elif self.level == 9:
            self.place_monsters(Abomination)
        elif self.level == 1:#MAX_DLEVEL:
            self.place_monsters(TrollKing)

    def find_tile(self, func):
        for x in range(MAP_W):
            for y in range(MAP_H):
                tile = self.tiles[x][y]
                if func(tile):
                    return (x, y, tile)

    def recalc_fov(self):
        T.map_compute_fov(self.fov_map,
                                self.player.x, self.player.y,
                                MAP_W,
                                True)
        for x in range(MAP_W):
            for y in range(MAP_H):
                if self.is_visible(x, y):
                    self.tiles[x][y].remember_glyph()

    def is_visible(self, x, y):
        return T.map_is_in_fov(self.fov_map, x, y) and \
            dist(x, y, self.player.x, self.player.y) <= \
            self.player.fov_range + self.player.radius

    def neighbor_tiles(self, x, y):
        for dx, dy in ALL_DIRS:
            if self.in_map(x+dx, y+dy):
                yield self.tiles[x+dx][y+dy]

    def do_turn(self, t):
        for mob in self.mobs:
            mob.heartbeat()
            if mob.speed < 0 and \
                    t % (6 + max(mob.speed, MIN_SPEED)) == 0:
                continue
            mob.act()
            if mob.speed > 0 and \
                    t % (6 - min(mob.speed, MAX_SPEED)) == 0:
                mob.act()

    def populate(self):
        n_monsters = 3 + roll(2, self.level)
        n_items = roll(2, 4, 1)
        for i in range(n_monsters):
            mcls = random_by_level(self.level, Monster.ALL)
            self.place_monsters(mcls)
        for i in range(n_items):
            x, y, tile = self.random_empty_tile(no_mob=False, no_stair=True)
            item = random_by_level(self.level, Item.ALL)()
            tile.items.append(item)
        for i in range(5):
            self.add_chest(self.level)
        self.add_shrine()
        

    def flood(self, x, y, mcls, n):
        if n == 0:
            return n
        if x < 0 or x >= MAP_W or y < 0 or y >= MAP_H:
            return n
        tile = self.tiles[x][y]
        if tile.mob or not tile.walkable:
            return n
        mcls().put(self, x, y)
        n -= 1
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        shuffle(dirs)
        for dx, dy in dirs:
            n = self.flood(x+dx, y+dy, mcls, n)
        return n

    def place_monsters(self, mcls, *args, **kwargs):
        x, y, tile = self.random_empty_tile(*args, **kwargs)
        self.flood(x, y, mcls, mcls.multi)

    def random_empty_tile(self, no_mob=True, not_seen=False, no_stair=False):
        from maps.tiles import StairUpTile
        while True:
            x, y = randrange(MAP_W), randrange(MAP_H)
            tile = self.tiles[x][y]
            if not tile.walkable:
                continue
            if no_mob and tile.mob:
                continue
            if not_seen and self.is_visible(x, y):
                continue
            if no_stair and isinstance(tile, StairUpTile):
                continue
            return (x, y, tile)

    def in_map(self, x, y):
        return 0 <= x < MAP_W and 0 <= y < MAP_H

    def place_obj(self, x, y, obj):
        tile = self.tiles[x][y]
        tile.obj = obj()
        
    def add_shrine(self):
        x, y, _ = self.random_empty_tile()
        i = rand(1, 3)
        if i == 1:
            self.place_obj(x, y, LifeShrine)
        elif i == 2:
            self.place_obj(x, y, ManaShrine)
        else:
            self.place_obj(x, y, RefillingShrine)
            
    def add_chest(self, map_level):
        x, y, _ = self.random_empty_tile()
        if map_level == 1:
            i = rand(1, 4)
            if i == 1:
                self.place_obj(x, y, CopperTrunk)
            else:
                self.place_obj(x, y, WoodenBox)
        elif map_level in [2, 3, 4]:
            i = rand(1, 7)
            if i == 1:
                self.place_obj(x, y, SilverStrongbox)
            else:
                self.place_obj(x, y, CopperTrunk)
        elif map_level in [5, 6, 7, 8]:
            i = rand(1, 5)
            if i == 1:
                self.place_obj(x, y, CopperTrunk)
            else:
                self.place_obj(x, y, SilverStrongbox)
        elif map_level in [9, 10, 11]:
            i = rand(1, 4)
            if i == 1:
                self.place_obj(x, y, GoldenRelicBox)
            else:
                self.place_obj(x, y, SilverStrongbox)
        elif map_level == MAX_DLEVEL:
            i = rand(1, 3)
            if i == 1:
                self.place_obj(x, y, RunedChest)
            else:
                self.place_obj(x, y, GoldenRelicBox)




















