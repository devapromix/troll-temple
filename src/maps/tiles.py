import tcod as T
from maps.tile import Tile

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