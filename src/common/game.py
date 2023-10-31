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

# --- COLOURS --- #

COLOR_ITEM    = T.light_grey
COLOR_TITLE   = T.lighter_yellow
COLOR_ALERT   = T.light_yellow
COLOR_ERROR   = T.lighter_red
COLOR_MAGIC   = T.lighter_blue
COLOR_VENOM   = T.lighter_green
COLOR_CONFUSE = T.lightest_blue

# --- CONSTANTS --- #

UNKNOWN_GLYPH = '?', COLOR_ERROR

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
    ([pygame.K_q],      'quit'),
    ([pygame.K_COMMA],  'ascend'),
    ([pygame.K_SLASH],  'help'),
    ([pygame.K_g],      'pick_up'),
    ([pygame.K_u],      'use_map_object'),
    ([pygame.K_i],      'inventory'),
    ([pygame.K_p],      'character'),
    ([pygame.K_b],      'spellbook'),
    ([pygame.K_s],      'select'),
    ([pygame.K_c],      'craftbox'),
    ([pygame.K_d],      'drop'),
    ([pygame.K_t],      'test'),
    ([pygame.K_l],      'look'),
    ([pygame.K_w],      'wizard'),
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

class Game(object):
    def __init__(self, wizard):
        # from mobs import mobs
        from mobs.player import FIGHTER
        self.wizard = wizard
        self.wizard = True
        self.selected_game_class = FIGHTER
        self.keydown = None

    def play(self):
        init(self)
        title_screen()
        intro_screen()
        select_game_class_screen()
        self.start()
        self.loop()
        close()

    def start(self):
        from mobs.player import Player
        self.player = Player(self.wizard, self.selected_game_class)
        self.turns = 0
        self.welcome()
        self.start_map(1)

    def start_map(self, level):
        from .maps import Map
        self.map = Map(level)
        x, y, _ = self.map.random_empty_tile()
        self.player.put(self.map, x, y)

    def ascend(self):
        self.turns += 1
        self.start_map(self.map.level + 1)


    def loop(self):
        draw_all()
        try:
            while True:
                if self.player.death:
                    if self.wizard:
                        if prompt('Die? (Y/N)', [pygame.K_y, pygame.K_n]) == pygame.K_n:
                            new_ui_turn()
                            self.player.resurrect()
                            message('You are resurrected!', COLOR_ERROR)
                            draw_all()
                            continue
                    prompt(
                        'Game over: %s. Press ENTER' % self.player.death,
                        [pygame.K_RETURN])
                    raise Quit()
                if self.player.won:
                    prompt(
                        'Congratulations! You have won. Press ENTER',
                        [pygame.K_RETURN])
                    raise Quit()
                while self.player.action_turns > 0:
                    for i in pygame.event.get():
                        if i.type == pygame.KEYUP:
                            self.do_command(i.key)
                            self.keydown = None
                        if i.type == pygame.KEYDOWN:
                            self.keydown = i.key
                    if self.keydown != None:
                        self.do_walk_command(self.keydown)
                self.map.do_turn(self.turns)
                self.turns += 1
                #draw_all()
                pygame.time.delay(DELAY)
        except Quit:
            pass

    def do_walk_command(self, key):
        cmd = decode_walk_key(key)
        if cmd is None:
            return
        new_ui_turn()
        if isinstance(cmd, str):
            getattr(self, 'cmd_'+cmd)()
        else:
            name, args = cmd
            getattr(self, 'cmd_'+name)(*args)
        draw_all()

    def do_command(self, key):
        cmd = decode_interface_key(key)
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

    def cmd_pick_up(self):
        tile = self.player.tile
        if tile.items == []:
            message('There is nothing here to pick up.', COLOR_ERROR)
        elif len(tile.items) == 1:
            self.player.pick_up(tile.items[0])
        else:
            while True and tile.items:
                item = select_item('Select an item to pick up, ESC to exit',
                                      tile.items)
                if item:
                    self.player.pick_up(item)
                    draw_all()
                else:
                    break

    def cmd_drop(self):
        item = select_item('Select an item to drop, ESC to exit', self.player.items)
        if item:
            self.player.drop(item)

    def cmd_inventory(self):
        item = select_item('Select an item to use, ESC to exit', self.player.items, True)
        if item:
            self.player.use(item)

    def cmd_use_map_object(self):
        from maps.objects import MapObject
        if self.player.tile.obj == None or not issubclass(self.player.tile.obj, MapObject):
            message('Stand on a map object to use.', COLOR_ERROR)
            return
        
        self.player.tile.obj.on_enter(self, self.player)

    def cmd_ascend(self):
        from .maps import StairUpTile
        if not isinstance(self.player.tile, StairUpTile):
            message('Stand on a up stairway to ascend.', COLOR_ERROR)
            return

        message('You take a moment to rest, and recover your strength.', T.yellow)
        self.player.heal(int(self.player.max_hp / 2))
        self.player.mana.fill()
        message('After a rare moment of peace, you ascend higher into the heart of the Temple...', T.yellow)
        self.ascend()

    def cmd_quit(self):
        if prompt('Quit? (Y/N)', [pygame.K_y, pygame.K_n]) == pygame.K_y:
            raise Quit()
        else:
            new_ui_turn()
            
    def cmd_select(self):
        pass

    def cmd_wizard(self):
        if self.wizard and self.map.level < MAX_DLEVEL:
            self.start_map(self.map.level+1)

    def cmd_look(self):
        look_mode()
        
    def cmd_help(self):
        intro_screen()
        
    def cmd_spellbook(self):
        if self.player.has_spellbook:
            spell = select_spell('Select a spell to cast, ESC to exit', self.player.spells)
            if spell:
                self.player.use_spell(spell)
        else:
            message("You don't have a spellbook!", COLOR_ERROR)

    def cmd_craftbox(self):
        if self.player.has_craftbox:
            recipe = select_recipe('Select a recipe to craft, ESC to exit', self.player.recipes)
            if recipe:
                self.player.craft(recipe)
        else:
            message("You don't have a craftbox!", COLOR_ERROR)

    def cmd_character(self):
        character_screen()

    def cmd_test(self):
        if self.wizard:
            pass

    def welcome(self):
        message("Brave adventurer, you are now lost in the underground corridors of the Old Temple.", T.yellow)
        message("There is no way to return to your homeland.", T.yellow)
        message("How long can you survive?", T.yellow)

# --- GAME --- #

def out(x, y, text, color = T.white, bkcolor = T.black):
    _txt = GAME.font.render(str(text), True, color, bkcolor)
    if x == 0:
        SCREEN.blit(_txt, (int((SCREEN_W - (_txt.get_width() / GAME.font_width))/2) * GAME.font_width, y * GAME.font_height))
    else:
        SCREEN.blit(_txt, (x * GAME.font_width, y * GAME.font_height))
    
def clear():
    SCREEN.fill(T.black)
    
def refresh():
    pygame.display.flip()
    
def init(game):
    global MESSAGES, GAME, SCREEN
    GAME = game
    MESSAGES = []
    pygame.init()
    #GAME.duneon_tileset = pygame.image.load("../assets/images/dungeon.png")
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
    #SCREEN.blit(GAME.duneon_tileset, (0,0))
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
            out(x+1, y+1, c, color)
                                  
def _draw_bar(x, y, cur, max, color):
    r = 0
    w = round(cur * 18 / max)
    for r in range(w):
        out(r + 60 + x + 2, y, "=", color)
    out(79, y, "[", T.dark_grey)
    out(98, y, "]", T.dark_grey)

def _draw_status():
    from mobs.player import GAME_CLASSES
    out(60, 1, "Troll Temple" + " (" +  "Level: " + str(GAME.map.level) + ")", T.light_green) 
    _game_class = GAME_CLASSES[GAME.player.game_class - 1]
    out(60, 3, GAME.player.name + " " + _game_class[0] + " Level " + str(GAME.player.level), _game_class[2])
    out(60, 5, "Exp.:   " + str(GAME.player.exp) + "/" + str(GAME.player.max_exp()), T.light_grey)    
    _draw_bar(18, 5, GAME.player.exp, GAME.player.max_exp(), T.light_yellow)
    out(60, 6, "Health: " + str(round(GAME.player.hp)) + "/" + str(GAME.player.max_hp), T.light_grey)    
    _draw_bar(18, 6, GAME.player.hp, GAME.player.max_hp, T.light_red)
    out(60, 7, "Mana:   " + GAME.player.mana.to_string(), T.light_grey)    
    _draw_bar(18, 7, GAME.player.mana.cur, GAME.player.mana.max, T.light_blue)
    out(60, 8, "Damage: " + describe_dice(*GAME.player.dice) + " Armor: " + str(GAME.player.armor) + " Turns:  " + str(GAME.turns), T.light_grey)

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

def message(s, color = T.white):
    s = s[0].upper() + s[1:]
    print(s)
    MESSAGES.append((True, s, color))
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
        out(5, i+3, spell.descr, T.light_grey)

def spellbook(title='Spellbook', spells=None):
    _draw_spellbook(title, spells or GAME.player.spells)
    _draw_messages()
    _draw_status()
    refresh()   

# --- CHARACTER --- #

def character_screen():
    from mobs.player import GAME_CLASSES
    from common.calendar import Calendar
    calendar = Calendar()
    clear()
    _game_class = GAME_CLASSES[GAME.player.game_class - 1]
    out(2, 1, GAME.player.name, COLOR_TITLE)

    out(2, 3,  "Race         " + "Human", T.light_grey)
    out(2, 4,  "Class        " + _game_class[0], T.light_grey)
    out(2, 6,  "Level        " + str(GAME.player.level), T.light_grey)
    out(2, 7,  "Experience   " + str(GAME.player.exp) + "/" + str(GAME.player.max_exp()), T.light_grey)
    if GAME.player.hp_regen > 0:
        regen =  " (+" + str(GAME.player.hp_regen) + ")"
    else:
        regen = ""
    out(2, 9,  "Health       " + str(round(GAME.player.hp)) + "/" + str(GAME.player.max_hp) + regen, T.light_grey)
    if GAME.player.mana_regen > 0:
        regen =  " (+" + str(GAME.player.mana_regen) + ")"
    else:
        regen = ""
    out(2, 10, "Mana         " + GAME.player.mana.to_string() + regen, T.light_grey)
    out(2, 12, "Damage       " + describe_dice(*GAME.player.dice) + " (" + str_dice(*GAME.player.dice) + ")", T.light_grey)
    out(2, 13, "Armor        " + str(GAME.player.armor), T.light_grey)
    out(2, 15, "Speed        " + str(GAME.player.speed), T.light_grey)
    out(2, 16, "Magic power  " + str(GAME.player.magic), T.light_grey)
    out(2, 17, "Light radius " + str(GAME.player.fov_range + GAME.player.radius), T.light_grey)
    out(2, 18, "", T.light_grey)
    out(2, 19, "", T.light_grey)
    out(2, 20, "", T.light_grey)
    out(2, 21, "", T.light_grey)
    out(2, 22, "", T.light_grey)
    out(2, 24, "Turns        " + str(GAME.turns), T.light_grey)
    out(2, 25, "Kills        " + str(GAME.player.kills), T.light_grey)
    if GAME.wizard:
        out(2, 26, "Deaths       " + str(GAME.player.deaths), T.light_grey)

    out(35, 3, calendar.get_time_date(GAME.turns), T.light_grey)

    out(0, 28, "Press ENTER to continue...", T.light_grey)
    refresh()
    anykey()

# --- UI --- #

def draw_all():
    clear()
    _draw_map()
    _draw_messages()
    _draw_status()
    refresh()

def _draw_game_class_screen():
    from mobs.player import GAME_CLASSES, FIGHTER, THIEF, RANGER, MAGE
    clear()
    out(2, 1, "Choose your class", COLOR_TITLE)
    for i, game_class in enumerate(GAME_CLASSES):
        out(3, i + 3, chr(i + ord('a')), T.light_grey) 
        if GAME.selected_game_class == i + 1:
            out(1, i + 3, '>', T.white)
            out(5, i + 3, game_class[0], T.white) 
        else:
            out(5, i + 3, game_class[0], game_class[2])

    if GAME.selected_game_class == FIGHTER:
        out(20, 3, "Fighters are the most powerful class in the game. Thanks to strong", T.white)
        out(20, 4, "armor and a large amount of life, warriors are indispensable in", T.white)
        out(20, 5, "battles and can withstand the onslaught of the enemy for a long time.", T.white)
        out(20, 6, "They are masters of close combat and are excellent with a sword,", T.white)
        out(20, 7, "hammer or axe. With their strong blows, they can cause damage to", T.white)
        out(20, 8, "several enemies at once, or they can focus on one.", T.white)
        out(20, 10, "Weapon: " + "short sword", T.white)
        out(20, 11, "Armor: " + "ring mail, round shield", T.white)
        out(20, 13, "Leather sack", T.white)
    elif GAME.selected_game_class == THIEF:
        out(20, 3, "Thieves specialize in one-on-one combat. They are capable of destroying", T.white)
        out(20, 4, "an enemy with a single attack, after immobilizing him with a sudden", T.white)
        out(20, 5, "stun or knocking him down. In addition, they have the ability to", T.white)
        out(20, 6, "increase critical strike chance and speed. A dagger in the hands of a", T.white)
        out(20, 7, "thief turns into a fast, deadly weapon that strikes enemies to the very", T.white)
        out(20, 8, "heart. And only thieves can safely pick locks and bypass traps.", T.white)
        out(20, 10, "Weapon: " + "small dagger", T.white)
        out(20, 11, "Armor: " + "shadow armor", T.white)
        out(20, 13, "Snakeskin knapsack, alchemy set", T.white)
    elif GAME.selected_game_class == RANGER:
        out(20, 3, "Rangers are incredibly destructive in combat and strike terror and fear", T.white)
        out(20, 4, "into their enemies with their immense strength and incredible speed.", T.white)
        out(20, 5, "Thanks to a large number of skills that attack a single target, they", T.white)
        out(20, 6, "are able to trackdown the victim and kill them at the right moment.", T.white)
        out(20, 7, "Enemies will meet their death by dying from a huge number of wounds", T.white)
        out(20, 8, "and bleeding, causing damage over time.", T.white)
        out(20, 10, "Weapon: " + "hunting spear", T.white)
        out(20, 11, "Armor: " + "quilted armor", T.white)
        out(20, 13, "Master's haversack, light quiver, craft box", T.white)
    elif GAME.selected_game_class == MAGE:
        out(20, 3, "Mages have knowledge of ancient spells and can call upon the power", T.white)
        out(20, 4, "of the elements to help them. They are capable of dealing massive", T.white)
        out(20, 5, "damage to a large number of enemies, as well as slowing, pinning and", T.white)
        out(20, 6, "knocking back enemies. Magicians use staves and magical artifacts", T.white)
        out(20, 7, "as weapons, which give them strength and unity with the energy flows", T.white)
        out(20, 8, "of the world.", T.white)
        out(20, 10, "Weapon: " + "short staff", T.white)
        out(20, 11, "Armor: " + "cultist robe", T.white)
        out(20, 13, "Linen bag, spellbook", T.white)

    out(0, 28, "Press ENTER to continue...", T.light_grey)
    refresh()

def title_screen():
    clear()

    out(5, 4,  '##### ####   ###  #     #', T.green)
    out(5, 5,  '# # # #   # #   # #     #', T.green)
    out(5, 6,  '  #   ####  #   # #     #', T.green)
    out(5, 7,  '  #   # #   #   # #     #', T.green)
    out(5, 8,  '  #   #  #   ###  ##### #####', T.green)

    out(10, 10,  '##### ##### #     # ##### #     #####', T.light_red)
    out(10, 11,  '# # # #     ##   ## #   # #     #', T.light_red)
    out(10, 12,  '  #   ###   # # # # ####  #     ###', T.light_red)
    out(10, 13,  '  #   #     #  #  # #     #     #', T.light_red)
    out(10, 14,  '  #   ##### #     # #     ##### #####', T.light_red)

    out(35, 17,  ' v.' + VERSION, T.light_green)

    out(10, 22,  'by Apromix <maxwof@ukr.net>', T.light_yellow)

    out(48, 4,  '                        /\ ', T.darker_yellow)
    out(48, 5,  '                      _/--\ ', T.darker_yellow)
    out(48, 6,  '                     /     O ', T.darker_yellow)
    out(48, 7,  '               /\   /       \ ', T.darker_yellow)
    out(48, 8,  '             _/| \_/      _  \ ', T.darker_yellow)
    out(48, 9,  '            /     /     _/ \  \ ', T.darker_yellow)
    out(48, 10, '         __/  ___/     /    \  ) ', T.darker_yellow)
    out(48, 11, '        y       Λ     |      | | ', T.darker_yellow)
    out(48, 12, '       ,       / \   /       | | ', T.darker_yellow)
    out(48, 13, '      /        \  \  |        \( ', T.darker_yellow)
    out(48, 14, '     /             \|          | \ ', T.darker_yellow)
    out(45, 15, '       ,___|_  _|-----`__ |-|- __|__,---', T.darker_yellow)
    out(45, 16, '      ._/ /                 \____/      \, ', T.darker_yellow)
    out(45, 17, '     /  \ \                  \```\        \, ', T.darker_yellow)
    out(45, 18, '    (__   _\                 |```|         L_, ', T.darker_yellow)
    out(45, 19, '    /   ./ /       /\         \```\       /  _\ ', T.darker_yellow)
    out(45, 20, '   |   /  /       /  \        |```|       \,   | ', T.darker_yellow)
    out(45, 21, '  /  (                |       \```\       /  _/ \ ', T.darker_yellow)
    out(45, 22, ' /                            |```|           _,| ', T.darker_yellow)
    out(45, 23, ' |_                           \```\             \ ', T.darker_yellow)

    out(0, 28, "Press ENTER to continue...", T.light_grey)
    refresh()
    anykey()

def intro_screen():
    clear()
    
    out(0, 2, "Many centuries ago...", COLOR_TITLE)
    
    out(13, 4, "You are a young adventurer who has entered the abandoned Old Temple in Lonely Mountain. ", T.lighter_grey)
    out(10, 5, "Many horror stories were told about this Temple at nighttime bonfires, as well as stories", T.lighter_grey)
    out(10, 6, "about a Ruby Amulet that could grant great power to its wearer. As an intrepid explorer,", T.lighter_grey)
    out(10, 7, "you grab your trusty sword and enter the Old Temple to find out what really lurks in its", T.lighter_grey)
    out(10, 8, "dark shadows. Use your wits to collect items to explore the levels of the Old Temple.", T.lighter_grey)
    out(13, 10, "However, be aware that many dangers await you. Good luck! You will need it...", T.lighter_grey)

    out(13, 13, "Keybindings:", T.lighter_grey)
    out(15, 15, "[I] show inventory", T.lighter_grey)
    out(15, 16, "[G] pick up an item from the floor", T.lighter_grey)
    out(15, 17, "[D] drop an item to the floor", T.lighter_grey)
    out(15, 18, "[L] use look mode", T.lighter_grey)
    out(15, 19, "[S] use shoot mode", T.lighter_grey)
    out(15, 20, "[<] go up stairs", T.lighter_grey)
    out(15, 21, "[U] use map object (portal, shrine)", T.lighter_grey)
    out(15, 22, "[?] show this help screen", T.lighter_grey)
    out(15, 23, "[5] wait one turn", T.lighter_grey)
    out(15, 24, "[M] view last messages", T.lighter_grey)
    out(15, 25, "[Q] quit game", T.lighter_grey)
    
    out(55, 15, "[A] open alchemyset (only thief class)", T.lighter_grey)
    out(55, 16, "[C] open craftbox (only ranger class)", T.lighter_grey)
    out(55, 17, "[B] open spellbook (only mage class)", T.lighter_grey)
    out(55, 18, "[P] open character sheet", T.lighter_grey)


    out(0, 28, "Press ENTER to continue...", T.light_grey)
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

def look_mode(shoot = False):
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

def select_item(title, items, flag = False):
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
            if 0 <= i < len(spells):
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
                    return
def prompt(s, choices = None):
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
        if event.type == pygame.KEYUP:
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