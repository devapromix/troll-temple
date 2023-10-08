import tcod as T
from bearlibterminal import terminal as B
from utils import *
from random import choice

# --- CONSTANTS --- #

VERSION = '0.7'

SCREEN_W = 100
SCREEN_H = 30

MAP_W = 60 - 2
MAP_H = SCREEN_H - 2

BUFFER_H = SCREEN_H // 2 + 1

TITLE = 'Troll Caves'

UNKNOWN_GLYPH = '?', T.red

MAX_SPEED = 5
MIN_SPEED = -4

MAX_DLEVEL = 12

INVENTORY_SLOTS = {
    'w': 'wielded',
    'l': 'carried as light source',
    'a': 'being worn',
    'b': 'being worn',
}

STATUS_W = SCREEN_W - MAP_W - 2
STATUS_H = 10

INV_SIZE = SCREEN_H - 4
INV_W = SCREEN_W
INV_H = INV_SIZE + 3

BOOK_SIZE = SCREEN_H - 4

# --- KEYS --- #

KEYS = [
    ([B.TK_KP_7], ('walk', (-1, -1))),
    ([B.TK_KP_8, B.TK_UP], ('walk', (0, -1))),
    ([B.TK_KP_9], ('walk', (1, -1))),
    ([B.TK_KP_4, B.TK_LEFT], ('walk', (-1, 0))),
    ([B.TK_KP_5], 'wait'),
    ([B.TK_KP_6, B.TK_RIGHT], ('walk', (1, 0))),
    ([B.TK_KP_1], ('walk', (-1, 1))),
    ([B.TK_KP_2, B.TK_DOWN], ('walk', (0, 1))),
    ([B.TK_KP_3], ('walk', (1, 1))),

    ([B.TK_ESCAPE], 'quit'),
    ([B.TK_PERIOD], 'descend'),
    ([B.TK_G], 'pick_up'),
    ([B.TK_I], 'inventory'),
    ([B.TK_B], 'spellbook'),
    ([B.TK_D], 'drop'),
    ([B.TK_T], 'test'),
    ([B.TK_L], 'look'),
    ([B.TK_W], 'wizard'),
]

def decode_key(key):
    for keys, cmd in KEYS:
        if key in keys:
            return cmd
    return None

# --- QUIT --- #

class Quit(Exception):
    pass

# --- GAME --- #

class Game(object):
    def __init__(self, wizard):
        import mobs
        self.wizard = wizard
        self.wizard = True
        self.selected_game_class = mobs.FIGHTER

    def play(self):
        init(self)
        title_screen()
        intro_screen()
        select_game_class_screen()
        self.start()
        self.loop()
        close()

    def start(self):
        from mobs import Player
        self.player = Player(self.wizard, self.selected_game_class)
        self.turns = 0
        message("Welcome to " + TITLE + "!")
        self.start_map(1)

    def start_map(self, level):
        from maps import Map
        self.map = Map(level)
        x, y, _ = self.map.random_empty_tile()
        self.player.put(self.map, x, y)

    def loop(self):
        draw_all()
        try:
            while True:
                if self.player.death:
                    if self.wizard:
                        if prompt('Die? (Y/N)', [B.TK_Y, B.TK_N]) == B.TK_N:
                            new_ui_turn()
                            self.player.resurrect()
                            message('You are resurrected!', T.pink)
                            draw_all()
                            continue
                    prompt(
                        'Game over: %s. Press ENTER' % self.player.death,
                        [B.TK_ENTER, B.TK_RETURN])
                    raise Quit()
                if self.player.won:
                    prompt(
                        'Congratulations! You have won. Press ENTER',
                        [B.TK_ENTER, B.TK_RETURN])
                    raise Quit()
                while self.player.action_turns > 0:
                    key = readkey()
                    self.do_command(key)
                self.map.do_turn(self.turns)
                self.turns += 1
                draw_all()
        except Quit:
            pass

    def do_command(self, key):
        cmd = decode_key(key)
        if cmd is None:
            return
        new_ui_turn()
        if isinstance(cmd, str):
            getattr(self, 'cmd_'+cmd)()
        else:
            name, args = cmd
            getattr(self, 'cmd_'+name)(*args)
        draw_all()

    def cmd_walk(self, dx, dy):
        self.player.walk(dx, dy)

    def cmd_wait(self):
        self.player.wait()

    def cmd_pick_up(self):
        tile = self.player.tile
        if tile.items == []:
            message('There is nothing here to pick up.')
        elif len(tile.items) == 1:
            self.player.pick_up(tile.items[0])
        else:
            while True and tile.items:
                item = select_item('Select an item to pick up',
                                      tile.items)
                if item:
                    self.player.pick_up(item)
                    draw_all()
                else:
                    break

    def cmd_drop(self):
        item = select_item('Select an item to drop', self.player.items)
        if item:
            self.player.drop(item)

    def cmd_inventory(self):
        item = select_item('Select an item to use', self.player.items, True)
        if item:
            self.player.use(item)

    def cmd_descend(self):
        from maps import StairDownTile
        if not isinstance(self.player.tile, StairDownTile):
            message('Stand on a down stairway to descend.')
            return

        self.player.heal(int(self.player.max_hp / 2))
        message('You take a moment to rest, and recover your strength.')
        self.turns += 1
        self.start_map(self.map.level + 1)
        message('After a rare moment of peace, you descend deeper into the heart of the dungeon...')

    def cmd_quit(self):
        if prompt('Quit? (Y/N)', [B.TK_Y, B.TK_N]) == B.TK_Y:
            raise Quit()
        else:
            new_ui_turn()

    def cmd_wizard(self):
        if self.wizard and self.map.level < MAX_DLEVEL:
            self.start_map(self.map.level+1)

    def cmd_look(self):
        look_mode()
        
    def cmd_spellbook(self):
        if self.player.has_spellbook:
            spell = select_spell('Select a spell to cast', self.player.spells)
            if spell:
                self.player.use_spell(spell)
        else:
            message("You don't have a spellbook!")

    def cmd_test(self):
        if self.wizard:
            pass

# --- GAME --- #

def set_color(c):
    B.color(B.color_from_argb(255, c.r, c.g, c.b))
    
def set_bkcolor(c):
    B.bkcolor(B.color_from_argb(255, c.r, c.g, c.b))
    
def init(game):
    global MESSAGES, GAME
    GAME = game
    MESSAGES = []
    B.open()
    wiz_str = ""
    if GAME.wizard:
        wiz_str = " [WIZARD]"
    B.set("window: size=" + str(SCREEN_W) + "x" + str(SCREEN_H) + ", cellsize=auto, title='" + TITLE + " v." + VERSION + wiz_str + "'")
    B.color("white")

def close():
    GAME = None
    B.close()

# --- UI --- #

def _draw_map():
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
            set_color(color)
            B.print(x+1, y+1, c)
                                  
def _draw_bar(x, y, cur, max):
    r = 0
    w = round(cur * 18 / max)
    for r in range(w):
        B.print(r + 60 + x + 2, y, "=")
    B.color("light grey")
    B.print(79, y, "[[")
    B.print(98, y, "]]")

def _draw_status():
    import mobs
    B.color("light green")
    B.print(60, 1, "Troll Temple" + " (" +  "Depth: " + str(GAME.map.level) + ")") 
    _game_class = mobs.GAME_CLASSES[GAME.player.game_class - 1]
    B.color(_game_class[2])
    B.print(60, 3, "Trollhunter" + " " + _game_class[0] + " Level " + str(GAME.player.level))
    B.color("light grey")
    B.print(60, 5, "Exp.:   " + str(GAME.player.exp) + "/" + str(GAME.player.max_exp()))    
    B.color("dark yellow")
    _draw_bar(18, 5, GAME.player.exp, GAME.player.max_exp())
    B.color("light grey")
    B.print(60, 6, "Health: " + str(round(GAME.player.hp)) + "/" + str(GAME.player.max_hp))    
    B.color("light red")
    _draw_bar(18, 6, GAME.player.hp, GAME.player.max_hp)
    B.color("light grey")
    B.print(60, 7, "Mana:   " + str(round(GAME.player.mp)) + "/" + str(GAME.player.max_mp))    
    B.color("light blue")
    _draw_bar(18, 7, GAME.player.mp, GAME.player.max_mp)
    B.color("light grey")
    B.print(60, 8, "Damage: " + describe_dice(*GAME.player.dice) + " Armor: " + str(GAME.player.armor) + " Speed: " + str(GAME.player.speed))
    deads = ""
    if GAME.wizard:
        deads = " Deads: " + str(GAME.player.deads)
    B.print(60, 9, "Turns:  " + str(GAME.turns) + " Kills: " + str(GAME.player.kills) + deads)
    B.print(60, 10, "Magic:  " + str(GAME.player.magic))

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
        set_color(color)
        B.print(60, i - start + 13, s)

def message(s, color = T.white):
    s = s[0].upper() + s[1:]
    print(s)
    MESSAGES.append((True, s, color))
    _draw_messages()
    B.refresh()

# --- INVENTORY --- #

def _draw_special_items():
    y = 3
    if GAME.player.has_spellbook or GAME.player.has_craftbox or GAME.player.has_alchemyset:
        B.color("white")
        B.print(45, 1, "Special items")
    if GAME.player.has_spellbook:
        B.color("light blue")
        B.print(45, y, "spellbook")
        y += 1
    if GAME.player.has_craftbox:
        B.color("dark yellow")
        B.print(45, y, "craftbox")
        y += 1
    if GAME.player.has_alchemyset:
        B.color("light green")
        B.print(45, y, "alchemyset")
        y += 1

def _draw_items(title, items):
    B.clear()
    B.color("white")
    B.print(2, 1, title)
    B.color("light grey")
    for i, item in enumerate(items):
        B.color("light grey")
        B.print(3, i + 3, chr(i + ord('a')))
        c, color = item.glyph
        set_color(color)
        B.print(5, i+3, chr(ord(c)))
        s = item.descr
        if GAME.player.has_equipped(item):
            B.color("white")
            B.print(1, i+3, '*')
        else:
            B.color("grey")
        B.print(7, i+3, s)

def draw_inventory(title='Inventory', items=None, flag=False):
    _draw_items(title, items or GAME.player.items)
    if flag:
        _draw_special_items()
    _draw_messages()
    _draw_status()
    B.refresh()

# --- SPELLBOOK --- #

def _draw_spellbook(title, spells):
    B.clear()
    B.color("white")
    B.print(2, 1, title)
    B.color("light grey")
    for i, spell in enumerate(spells):
        B.print(3, i + 3, chr(i + ord('a')))
        B.print(5, i+3, spell.descr)

def spellbook(title='Spellbook', spells=None):
    _draw_spellbook(title, spells or GAME.player.spells)
    _draw_messages()
    _draw_status()
    B.refresh()   

# --- UI --- #

def draw_all():
    B.clear()
    _draw_map()
    _draw_messages()
    _draw_status()
    B.refresh()

def select_game_class_screen():
    import mobs
    B.clear()
    
    B.color("light yellow")
    B.print(2, 1, "Choose your class")
    B.color("light grey")
    for i, game_class in enumerate(mobs.GAME_CLASSES):
        B.color("light grey")
        B.print(3, i + 3, chr(i + ord('a'))) 
        B.color(game_class[2])
        B.print(5, i + 3, game_class[0])    
    B.refresh()
    sel = select_game_class()
    GAME.selected_game_class = sel[1]

def intro_screen():
    B.clear()
    
    B.color("light yellow")
    B.print(SCREEN_W//2, 2, "Many centuries ago...", 0, 0, B.TK_ALIGN_CENTER)
    
    
    B.color("light grey")
    B.print(SCREEN_W//2, 28, "Press any key to continue...", 0, 0, B.TK_ALIGN_CENTER)
    B.refresh()
    anykey()

def title_screen():
    B.clear()

    B.color("darker green")
    B.print(5, 4,  '##### ####   ###  #     #')
    B.print(5, 5,  '  #   #   # #   # #     #')
    B.print(5, 6,  '  #   ####  #   # #     #')
    B.print(5, 7,  '  #   # #   #   # #     #')
    B.print(5, 8,  '  #   #  #   ###  ##### #####')

    B.color("dark yellow")
    B.print(15, 10,  ' ####  ###  #   # #####  ####')
    B.print(15, 11,  '#     #   # #   # #     #    ')
    B.print(15, 12,  '#     ##### #   # ###    ### ')
    B.print(15, 13,  '#     #   #  # #  #         #')
    B.print(15, 14,  ' #### #   #   #   ##### #### ')

    B.color("light blue")
    B.print(35, 17,  ' v.' + VERSION)

    B.color("dark red")
    B.print(10, 22,  'by Apromix <maxwof@ukr.net>')

    B.color("darker orange")
    B.print(45, 4,  '                           /\ ')
    B.print(45, 5,  '                         _/--\ ')
    B.print(45, 6,  '                        /     O ')
    B.print(45, 7,  '                  /\   /       \ ')
    B.print(45, 8,  '                _/| \_/      _  \ ')
    B.print(45, 9,  '               /     /     _/ \  \ ')
    B.print(45, 10, '            __/  ___/     /    \  ) ')
    B.print(45, 11, '           y       Λ     |      | | ')
    B.print(45, 12, '          ,       / \   /       | | ')
    B.print(45, 13, '         /        \  \  |        \( ')
    B.print(45, 14, '        /             \|          | \ ')
    B.print(45, 15, '       ,___|_  _|-----`__ |-|- __|__,---')
    B.print(45, 16, '      ._/ /                 \____/      \, ')
    B.print(45, 17, '     /  \ \                  \```\        \, ')
    B.print(45, 18, '    (__   _\                 |```|         L_, ')
    B.print(45, 19, '    /   ./ /       /\         \```\       /  _\ ')
    B.print(45, 20, '   |   /  /       /  \        |```|       \,   | ')
    B.print(45, 21, '  /  (                |       \```\       /  _/ \ ')
    B.print(45, 22, ' /                            |```|           _,| ')
    B.print(45, 23, ' |_                           \```\             \ ')

    B.color("light grey")
    B.print(SCREEN_W//2, 28, "Press any key to continue...", 0, 0, B.TK_ALIGN_CENTER)
    B.refresh()
    anykey()

def describe_tile(x, y):
    if GAME.map.is_visible(x, y):
        tile = GAME.map.tiles[x][y]
        message('%s.' % tile.name, tile.glyph[1])
        if tile.mob:
            message('%s.' % tile.mob.name, tile.mob.glyph[1])
        for item in tile.items:
            message('%s.' % item.descr, item.glyph[1])
    else:
        message('Out of sight.', T.grey)

def new_ui_turn():
    for i in reversed(list(range(len(MESSAGES)))):
        latest, s, color = MESSAGES[i]
        if latest:
            MESSAGES[i] = False, s, color
        else:
            break

# --- LOOK --- #

def look_mode():
    global MESSAGES
    from game import decode_key

    x, y, map = GAME.player.x, GAME.player.y, GAME.player.map
    _messages = MESSAGES
    MESSAGES = []
    message('Look mode - use movement keys, ESC to exit.', T.green)
    new_ui_turn()
    _draw_messages()
    redraw = True
    while True:
        if redraw:
            draw_all()
            char = B.pick(x+1, y+1)
            color = B.pick_color(x+1, y+1)

            B.color("black")
            B.bkcolor(color)
            B.put(x+1, y+1, char)
            
            B.refresh()
            B.bkcolor("black")
            describe_tile(x, y)

            _draw_messages()
            B.refresh()

            B.bkcolor('black')
            B.color(color)
            B.put(x+1, y+1, char);

            while MESSAGES and MESSAGES[-1][0]:
                MESSAGES.pop()
                
            redraw = False
        cmd = decode_key(readkey())
        if cmd == 'quit':
            break
        elif isinstance(cmd, tuple):
            name, args = cmd
            if name == 'walk':
                dx, dy = args
                if map.in_map(x + dx, y + dy):
                    x, y = x + dx, y + dy
                    redraw = True

    MESSAGES = _messages
    B.bkcolor("black")

# --- KEYS --- #

def select_item(title, items, flag = False):
    items = items[:INV_SIZE]
    draw_inventory(title, items, flag)
    key = readkey()
    if B.TK_A <= key <= B.TK_Z:
        i = key - B.TK_A
        if 0 <= i < len(items):
            return items[i]
    return None

def select_spell(title, spells):
    spells = spells[:BOOK_SIZE]
    spellbook(title, spells)
    key = readkey()
    if B.TK_A <= key <= B.TK_Z:
        i = key - B.TK_A
        if 0 <= i < len(spells):
            return spells[i]
    return None

def select_game_class():
    import mobs
    while True:
        _clear_buffer()
        key = readkey()
        if B.TK_A <= key <= B.TK_Z:
            i = key - B.TK_A
            if 0 <= i < len(mobs.GAME_CLASSES):
                return mobs.GAME_CLASSES[i]

def prompt(s, choices = None):
    message(s, T.green)
    draw_all()
    if choices:
        choices = list(choices)
        while True:
            key = readkey()
            if key in choices:
                return key
    else:
        return readkey()

def _clear_buffer():
    while B.has_input():
        key = B.read()

def readkey():
    key = B.read()
    _clear_buffer()
    return key

def anykey():
    _clear_buffer()
    while True:
        if B.has_input():
            break





