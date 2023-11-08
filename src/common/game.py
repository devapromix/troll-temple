import sys
import pygame
import tcod as T

from .utils import *

# --- CONSTANTS --- #

VERSION = '0.8'

SCREEN_W = 100
SCREEN_H = 30

MAP_W = 60 - 2
MAP_H = SCREEN_H - 2

DELAY = 100

BUFFER_H = SCREEN_H // 2 + 1

TITLE = 'Troll Temple'

MAX_SPEED = 5
MIN_SPEED = -4

MAX_DLEVEL = 12

INVENTORY_SLOTS = {
    'w': 'wielded',
    'o': 'wielded',
    'l': 'carried as light source',
    'r': 'ranged weapon',
    'q': 'quiver',
    'h': 'being worn',
    'a': 'being worn',
    'b': 'being worn',
}

STATUS_W = SCREEN_W - MAP_W - 2
STATUS_H = 10

INV_SIZE = SCREEN_H - 4
INV_W = SCREEN_W
INV_H = INV_SIZE + 3

BOOK_SIZE = SCREEN_H - 4

CRAFTBOX_SIZE = SCREEN_H - 4

# --- COLOURS --- #

COLOR_ITEM = T.light_grey
COLOR_TITLE = T.lighter_yellow
COLOR_ALERT = T.light_yellow
COLOR_ERROR = T.lighter_red
COLOR_MAGIC = T.lighter_blue

# --- KEYS --- #

pygame.init()

WALK_KEYS = [
    ([pygame.K_KP7], ('walk', (-1, -1))),
    ([pygame.K_KP8, pygame.K_UP], ('walk', (0, -1))),
    ([pygame.K_KP9], ('walk', (1, -1))),
    ([pygame.K_KP4, pygame.K_LEFT], ('walk', (-1, 0))),
    ([pygame.K_KP5], ('walk', (0, 0))),
    ([pygame.K_KP6, pygame.K_RIGHT], ('walk', (1, 0))),
    ([pygame.K_KP1], ('walk', (-1, 1))),
    ([pygame.K_KP2, pygame.K_DOWN], ('walk', (0, 1))),
    ([pygame.K_KP3], ('walk', (1, 1))),
]

KEYS = [
    ([pygame.K_q], 'quit'),
    ([pygame.K_COMMA], 'ascend'),
    ([pygame.K_SLASH], 'help'),
    ([pygame.K_g], 'pick_up'),
    ([pygame.K_u], 'use_map_object'),
    ([pygame.K_i], 'inventory'),
    ([pygame.K_p], 'character'),
    ([pygame.K_b], 'spellbook'),
    ([pygame.K_s], 'select'),
    ([pygame.K_c], 'craftbox'),
    ([pygame.K_d], 'drop'),
    ([pygame.K_t], 'test'),
    ([pygame.K_l], 'look'),
    ([pygame.K_w], 'wizard'),
]

LOOK_KEYS = WALK_KEYS + KEYS[:1] + [([pygame.K_ESCAPE], 'quit'), ([pygame.K_s], 'select')]


def decode_walk_key(key):
    return decode_key(key, WALK_KEYS)


def decode_interface_key(key):
    return decode_key(key, KEYS)


def decode_key(key, actions):
    for keys, cmd in actions:
        if key in keys:
            return cmd
    return None


# --- QUIT --- #

class Quit(Exception):
    pass


# --- GAME --- #


# --- GAME --- #

def out(x, y, text, color=T.white, bkcolor=T.black, w=0):
    _txt = GAME.font.render(str(text), True, color, bkcolor)
    if x == 0:
        SCREEN.blit(_txt, (
            int((SCREEN_W - (_txt.get_width() / GAME.font_width)) / 2) * GAME.font_width, y * GAME.font_height))
    elif w != 0:
        SCREEN.blit(_txt,
                    ((x + int((w - (_txt.get_width() / GAME.font_width)) / 2)) * GAME.font_width, y * GAME.font_height))
    else:
        SCREEN.blit(_txt, (x * GAME.font_width, y * GAME.font_height))


def out_text(x: int, y: int, width: int, text, color=T.white, bkcolor=T.black, w=0):
    last_space = 1
    last_drawed = -1
    line_count = 0
    for i, char in enumerate(text):
        if char == ' ':
            last_space = i
        if i - last_drawed >= width:
            out(x, y + line_count, text[last_drawed + 1: last_space], color, bkcolor)
            line_count += 1
            last_drawed = last_space

    if len(text) > last_drawed:
        out(x, y + line_count, text[last_drawed + 1:], color, bkcolor)
        line_count += 1

    return line_count


def out_file(x, y, filepath, color=T.white, bkcolor=T.black, w=0):
    with open(filepath, 'r') as f:
        for i, line in enumerate(f.readlines()):
            out(x, y + i, line.rstrip(), color, bkcolor, w)


def clear():
    SCREEN.fill(T.black)


def refresh():
    pygame.display.flip()


def init(game):
    global MESSAGES, GAME, SCREEN
    GAME = game
    MESSAGES = []
    pygame.init()
    # GAME.duneon_tileset = pygame.image.load("../assets/images/dungeon.png")
    GAME.font = pygame.font.Font("../assets/fonts/UbuntuMono-R.ttf", 16)
    _txt = GAME.font.render("W", True, T.white)
    GAME.font_width = _txt.get_width()
    GAME.font_height = _txt.get_height() + 1
    SCREEN = pygame.display.set_mode((SCREEN_W * GAME.font_width, SCREEN_H * GAME.font_height))
    wiz_str = ""
    if GAME.wizard:
        wiz_str = " [WIZARD]"
    pygame.display.set_caption(TITLE + " v." + VERSION + wiz_str)
    pygame.display.set_icon(pygame.image.load("../assets/icons/game.ico"))


def close():
    GAME = None
    pygame.quit()
    sys.exit()


# --- UI --- #

def _draw_map():
    # SCREEN.blit(GAME.duneon_tileset, (0,0))
    player = GAME.player
    for x in range(MAP_W):
        for y in range(MAP_H):
            tile = GAME.map.tiles[x][y]
            if GAME.map.is_visible(x, y):
                c, color = tile.visible_glyph
                d = dist(x, y, player.x, player.y)
                if d > player.light_range + 1:
                    color *= 0.6
            else:
                c, _ = tile.known_glyph
                color = T.dark_grey
            out(x + 1, y + 1, c, color)


def _draw_bar(x, y, cur, max, color):
    r = 0
    w = round(cur * 18 / max)
    for r in range(w):
        out(r + 60 + x + 2, y, "=", color)
    out(79, y, "[", T.dark_grey)
    out(98, y, "]", T.dark_grey)


def _draw_status():
    from mobs.player import GAME_CLASSES
    out(60, 1, "Troll Temple" + " (" + "Level: " + str(GAME.map.level) + ")", T.light_green)
    _game_class = GAME_CLASSES[GAME.player.game_class.value - 1]
    out(60, 3, GAME.player.name + " " + _game_class[0] + " Level " + str(GAME.player.level), _game_class[2])
    out(60, 5, "Exp.:   " + str(GAME.player.exp) + "/" + str(GAME.player.max_exp()), T.light_grey)
    _draw_bar(18, 5, GAME.player.exp, GAME.player.max_exp(), T.light_yellow)
    out(60, 6, "Life:   " + GAME.player.life.to_string(), T.light_grey)
    _draw_bar(18, 6, GAME.player.life.cur, GAME.player.life.max, T.light_red)
    out(60, 7, "Mana:   " + GAME.player.mana.to_string(), T.light_grey)
    _draw_bar(18, 7, GAME.player.mana.cur, GAME.player.mana.max, T.light_blue)
    out(60, 8, "Damage: " + describe_dice(*GAME.player.dice) + " Armor: " + str(GAME.player.armor) + " Turns:  " + str(
        GAME.turns), T.light_grey)

# --- MESSAGES --- #

def _draw_messages():
    n = len(MESSAGES)
    if n == 0:
        return
    start = max(n - BUFFER_H, 0)
    for i in range(start, n):
        latest, s, color = MESSAGES[i]
        if not latest:
            color *= 0.6
        out(60, i - start + 13, s, color)

def _split_message(text, width):
    n = -1
    lines = []
    words = text.split()
    def add(word):
        if len(lines[n]) == 0:
            lines[n] += word
        else:
            lines[n] += " " + word
    def new(n):
        lines.append("")
        n += 1
    new(n)
    for i, word in enumerate(words):
        if len(lines[n] + word) + 1 < width:
            add(word)
        else:
            new(n)
            add(word)
    return lines

def message(s, color = T.white):
    if 'MESSAGES' not in globals():
        print(s)
        return
    s = s[0].upper() + s[1:]
    lines = _split_message(s, 40)
    for i, line in enumerate(lines):
        print(line)
        MESSAGES.append((True, line, color))
    _draw_messages()
    refresh()

# --- INVENTORY --- #

def _item_color(item, color):
    if item.color != COLOR_ITEM:
        return item.color
    else:
        return color


def _draw_items(title, items):
    clear()
    out(2, 1, title, COLOR_TITLE)
    for i, item in enumerate(items):
        out(3, i + 3, chr(i + ord('a')), COLOR_ITEM)
        c, color = item.glyph
        out(5, i + 3, chr(ord(c)), color)
        s = item.descr
        if GAME.player.has_equipped(item):
            color = _item_color(item, T.white)
            out(1, i + 3, '*', T.white)
        else:
            color = _item_color(item, COLOR_ITEM)
        out(7, i + 3, s, color)


def draw_inventory(title='Inventory', items=None, flag=False):
    _draw_items(title, items or GAME.player.items)
    _draw_messages()
    _draw_status()
    refresh()


# --- SPELLBOOK --- #

def _draw_spellbook(title, spells):
    clear()
    out(2, 1, title, COLOR_TITLE)
    for i, spell in enumerate(spells):
        out(3, i + 3, chr(i + ord('a')), T.light_grey)
        out(5, i + 3, spell.descr, T.light_grey)


def spellbook(title='Spellbook', spells=None):
    _draw_spellbook(title, spells or GAME.player.spells)
    _draw_messages()
    _draw_status()
    refresh()


# --- CRAFTBOX --- #

def _draw_craftbox(title, recipes):
    clear()
    out(2, 1, title, COLOR_TITLE)
    for i, recipe in enumerate(recipes):
        out(3, i + 3, chr(i + ord('a')), T.light_grey)
        out(5, i + 3, recipe.descr, T.light_grey)


def craftbox(title='Craftbox', recipes=None):
    _draw_craftbox(title, recipes or GAME.player.recipes)
    _draw_messages()
    _draw_status()
    refresh()


def draw_statistics(y):
    out(40, y, "Statistics", COLOR_TITLE)
    out(40, y + 2, "Turns        " + str(GAME.turns), T.light_grey)
    out(40, y + 3, "Kills        " + str(GAME.player.kills), T.light_grey)
    if GAME.wizard:
        out(40, y + 6, "Deaths       " + str(GAME.stats.player_death_count), T.light_grey)
        
# --- UI --- #

def draw_all():
    clear()
    _draw_map()
    _draw_messages()
    _draw_status()
    refresh()


def _draw_game_class_screen():
    from mobs.player import GAME_CLASSES
    clear()
    out(2, 1, "Choose your class", COLOR_TITLE)
    for i, game_class in enumerate(GAME_CLASSES):
        out(3, i + 3, chr(i + ord('a')), T.light_grey)
        if GAME.selected_game_class.value == i + 1:
            out(1, i + 3, '>', T.white)
            out(5, i + 3, game_class[0], T.white)
            out_file(20, 3, '../assets/texts/class_' + game_class[0].lower() +'.txt', T.lighter_grey)
            out_file(70, 14, '../assets/texts/' + game_class[3].lower() +'.txt', game_class[2])
        else:
            out(5, i + 3, game_class[0], game_class[2])
    out(0, 28, "Press [ENTER] to continue...", T.light_grey)
    refresh()

def title_screen():
    clear()
    out_file(5, 4, '../assets/texts/troll.txt', T.green)
    out_file(45, 4, '../assets/texts/lonely_mountain.txt', T.darker_yellow)
    out_file(10, 10, '../assets/texts/temple.txt', T.light_red)
    out(35, 17, ' v.' + VERSION, T.light_green)
    out(6, 22, 'by Apromix and Gandifil', T.light_yellow)
    out(0, 28, "Press [ENTER] to continue...", T.light_grey)
    refresh()
    anykey()


def intro_screen():
    clear()
    out(0, 2, "Many centuries ago...", COLOR_TITLE)
    out_file(10, 4, '../assets/texts/help.txt', T.lighter_grey)
    out(0, 28, "Press [ENTER] to continue...", T.light_grey)
    refresh()
    anykey()


def select_game_class_screen():
    clear()
    _draw_game_class_screen()
    select_game_class()


def describe_tile(x, y):
    if GAME.map.is_visible(x, y):
        tile = GAME.map.tiles[x][y]
        message('%s.' % tile.name, tile.glyph[1])
        if tile.obj:
            message(tile.obj.name, tile.obj.glyph[1])
        if tile.mob:
            d = ""
            s = tile.mob.name
            if tile.mob.confused:
                d += "confused "
            elif tile.mob.poisoned > 0:
                d += "poisoned "
            if d != "":
                d = " (" + d.strip() + ")"
            s += d + "."
            message(s, tile.mob.glyph[1])
        for item in tile.items:
            message('%s.' % item.descr, item.glyph[1])
    else:
        message('Out of sight.', COLOR_ERROR)


def new_ui_turn():
    for i in reversed(list(range(len(MESSAGES)))):
        latest, s, color = MESSAGES[i]
        if latest:
            MESSAGES[i] = False, s, color
        else:
            break


# --- LOOK --- #

def look_mode(shoot=False):
    global MESSAGES

    x, y, map = GAME.player.x, GAME.player.y, GAME.player.map
    _messages = MESSAGES
    MESSAGES = []
    if shoot:
        message("Shoot mode - use movement keys", COLOR_TITLE)
        message("[S] to select target", COLOR_TITLE)
    else:
        message("Look mode - use movement keys", COLOR_TITLE)
    message("[ESC] to exit", COLOR_TITLE)
    new_ui_turn()
    _draw_messages()
    redraw = True

    while True:
        if redraw:
            draw_all()

            tile = map.tiles[x][y]
            if map.is_visible(x, y):
                char, color = tile.visible_glyph
                out(x + 1, y + 1, char, T.black, T.lighter_gray)
            refresh()
            describe_tile(x, y)

            _draw_messages()
            refresh()

            while MESSAGES and MESSAGES[-1][0]:
                MESSAGES.pop()

            redraw = False

        cmd = decode_key(readkey(), LOOK_KEYS)
        if cmd == 'quit':
            break
        elif cmd == 'select':
            tile = map.tiles[x][y]
            if tile.mob:
                return tile.mob
        elif isinstance(cmd, tuple):
            name, args = cmd
            if name == 'walk':
                dx, dy = args
                if map.in_map(x + dx, y + dy):
                    x, y = x + dx, y + dy
                    redraw = True

    MESSAGES = _messages


# --- KEYS --- #

def select_item(title, items, flag=False):
    items = items[:INV_SIZE]
    draw_inventory(title, items, flag)
    while True:
        key = readkey()
        if key in range(pygame.K_a, pygame.K_z):
            i = key - pygame.K_a
            if 0 <= i < len(items):
                return items[i]
        if key in [pygame.K_ESCAPE]:
            return None
    return None


def select_spell(title, spells):
    spells = spells[:BOOK_SIZE]
    spellbook(title, spells)
    while True:
        key = readkey()
        if key in range(pygame.K_a, pygame.K_z):
            i = key - pygame.K_a
            if 0 <= i < len(spells):
                return spells[i]
        if key in [pygame.K_ESCAPE]:
            return None
    return None


def select_recipe(title, recipes):
    recipes = recipes[:CRAFTBOX_SIZE]
    craftbox(title, recipes)
    while True:
        key = readkey()
        if key in range(pygame.K_a, pygame.K_z):
            i = key - pygame.K_a
            if 0 <= i < len(recipes):
                return recipes[i]
        if key in [pygame.K_ESCAPE]:
            return None
    return None


def select_game_class():
    from mobs.player import GAME_CLASSES
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                close()
            if event.type == pygame.KEYDOWN:
                if event.key in range(pygame.K_a, pygame.K_z):
                    i = event.key - pygame.K_a
                    if 0 <= i < len(GAME_CLASSES):
                        GAME.selected_game_class = GAME_CLASSES[i][1]
                        _draw_game_class_screen()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    pygame.event.clear()
                    return


def prompt(s, choices=None):
    if s != "":
        message(s, T.green)
        draw_all()
    if choices:
        choices = list(choices)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in choices:
                        pygame.event.clear()
                        return event.key
    else:
        return readkey()


def readkey():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.clear()
            close()
        if event.type == pygame.KEYDOWN:
            pygame.event.clear()
            return event.key


def anykey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                close()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    return



