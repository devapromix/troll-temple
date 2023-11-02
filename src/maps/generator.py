import tcod as T
from maps.tiles import *
from common.utils import *
from common.game import MAP_W, MAP_H, MAX_DLEVEL

class MapGenerator(object):

    def __init__(self):
        pass
        
    def generate(self, level):

        arr = array(MAP_W, MAP_H, lambda: ' ')
        rooms = []
        for i in range(500):
            w, h = randrange(5, 15), randrange(5, 10)
            room = self.try_put_room(arr, w, h)
            if room:
                rooms.append(room)

        if level < MAX_DLEVEL and level != 3 and level != 6 and level != 9:
            self.randomly_place(arr, StairUpTile.glyph[0])

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

        return self.array_to_tiles(arr)

    def array_to_tiles(self, arr):
        TILE_TABLE = {
            '.': FloorTile,
            '#': WoodWallTile,
            ' ': WallTile,
            '>': StairDownTile,
            '<': StairUpTile,
            }
        return [[TILE_TABLE[c]() for c in line] for line in arr]

    def try_put_room(self, arr, w, h):
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

    def print_array(self, arr):
        for y in range(len(arr[0])):
            for line in arr:
                stdout.write(line[y])
            stdout.write('\n')

    def randomly_place(self, arr, c):
        x, y = self.random_empty_space(arr)
        arr[x][y] = c

    def random_empty_space(self, arr):
        while True:
            x, y = randrange(MAP_W), randrange(MAP_H)
            if arr[x][y] == '.':
                return (x, y)








