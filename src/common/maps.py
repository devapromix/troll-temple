from mobs.mobs import *
from items.items import *
from common.game import *

# --- MAP --- #

class Map(object):
    def __init__(self, level):
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
        elif self.level == MAX_DLEVEL:
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

# --- TILE --- #

class Tile(object):
    walkable = True
    transparent = True
    glyph = UNKNOWN_GLYPH
    known_glyph = ' ', T.white

    def __init__(self):
        self.mob = None
        self.items = []

    @property
    def visible_glyph(self):
        if self.mob:
            if self.mob.poisoned > 0:
                return self.mob.glyph[0], COLOR_VENOM
            elif self.mob.confused:
                return self.mob.glyph[0], COLOR_CONFUSE
            else:
                return self.mob.glyph
        elif self.items:
            return self.items[-1].glyph
        else:
            return self.glyph

    def remember_glyph(self):
        if self.items:
            self.known_glyph = self.items[-1].glyph
        else:
            self.known_glyph = self.glyph

    def on_enter(self):
        pass

# --- TILES --- #

class FloorTile(Tile):
    name = 'floor'
    walkable = True
    transparent = True
    glyph = '.', T.grey

class WallTile(Tile):
    name = 'stone wall'
    walkable = False
    transparent = False
    glyph = '#', T.grey

class WoodWallTile(Tile):
    name = 'wooden wall'
    walkable = False
    transparent = False
    glyph = '#', T.dark_orange

class StairUpTile(Tile):
    name = 'stairs up'
    walkable = True
    transparent = True
    glyph = '<', T.light_grey

    def on_enter(self):
        message('There is a up stairway here.')

class StairDownTile(Tile):
    name = 'stairs down'
    walkable = True
    transparent = True
    glyph = '>', T.light_grey

    def on_enter(self):
        message('There is a down stairway here.')

# --- GENERATOR --- #

class MapGenerator(object):

    def __init__(self):
        print("generator")
        
    def generate(self, level):
        return generate_map(level)
        
def array_to_tiles(arr):
    TILE_TABLE = {
        '.': FloorTile,
        '#': WoodWallTile,
        ' ': WallTile,
        '>': StairDownTile,
        '<': StairUpTile,
        }
    return [[TILE_TABLE[c]() for c in line] for line in arr]

def try_put_room(arr, w, h):
    x1, y1 = randrange(MAP_W-w), randrange(MAP_H-h)
    for x in range(x1, x1+w):
        for y in range(y1, y1+h):
            if arr[x][y] != ' ':
                return None
    for x in range(x1, x1+w):
        for y in range(y1, y1+h):
            arr[x][y] = '.'
    for x in range(x1, x1+w):
        arr[x][y1] = '#'
        arr[x][y1+h-1] = '#'
    for y in range(y1, y1+h):
        arr[x1][y] = '#'
        arr[x1+w-1][y] = '#'
    return (x1, y1, w, h)

def print_array(arr):
    for y in range(len(arr[0])):
        for line in arr:
            stdout.write(line[y])
        stdout.write('\n')

def generate_map(level):
    arr = array(MAP_W, MAP_H, lambda: ' ')
    rooms = []
    for i in range(500):
        w, h = randrange(5, 15), randrange(5, 10)
        room = try_put_room(arr, w, h)
        if room:
            rooms.append(room)

    if level < MAX_DLEVEL and level != 3 and level != 6 and level != 9:
        randomly_place(arr, StairUpTile.glyph[0])

    costs = [(5, 40, 1),
             (5, 1, 2),
             (5, 40, 40)][3 * level // (MAX_DLEVEL + 1)]

    def corridor_path_func(x1, y1, x2, y2, data):
        if x2 == 0 or x2 == MAP_W-1 or y2 == 0 or y2 == MAP_H-1:
            return 0
        c = arr[x2][y2]
        if c == ' ':
            return costs[0]
        elif c == '#':
            return costs[1]
        else:
            return costs[2]


    path = T.path_new_using_function(
        MAP_W, MAP_H, corridor_path_func, None, 0.0)

    def connect(x1, y1, x2, y2):
        T.path_compute(path, x1, y1, x2, y2)
        for i in range(T.path_size(path)):
            x, y = T.path_get(path, i)
            c = arr[x][y]
            if c == '#' or c == ' ':
                arr[x][y] = '.'

    for i in range(len(rooms)-1):
        x1, y1, w1, h1 = rooms[i]
        x2, y2, w2, h2 = rooms[i+1]
        connect(x1+w1//2, y1+h1//2, x2+w2//2, y2+h2//2)

    T.path_delete(path)

    return array_to_tiles(arr)

def randomly_place(arr, c):
    x, y = random_empty_space(arr)
    arr[x][y] = c

def random_empty_space(arr):
    while True:
        x, y = randrange(MAP_W), randrange(MAP_H)
        if arr[x][y] == '.':
            return (x, y)