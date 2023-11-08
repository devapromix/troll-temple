import pygame
import tcod as T

from common.game import init, title_screen, intro_screen, select_game_class_screen, close, message, COLOR_ERROR, \
    draw_all, prompt, new_ui_turn, Quit, DELAY, decode_walk_key, decode_interface_key, select_item, look_mode, \
    MAX_DLEVEL, select_spell, select_recipe, character_screen
from common.stats import Stats
from graphics.scenes.choose_perk_scene import ChoosePerkScene


class Game(object):
    def __init__(self, wizard):
        from mobs.player import Classes
        self.wizard = wizard
        self.wizard = True
        self.selected_game_class = Classes.FIGHTER
        self.keydown = None
        self.stats = Stats()

    def play(self):
        init(self)
        title_screen()
        intro_screen()
        select_game_class_screen()
        self.start()
        self.cmd_perks()
        self.loop()
        close()

    def start(self):
        from mobs.player import Player
        self.player = Player(self.wizard, self.selected_game_class)
        self.player.on_die += lambda p, m: self.player_died(p, m)
        self.turns = 0
        self.welcome()
        self.start_map(1)

    def player_died(self, player, murderer):
        self.stats.player_death_count += 1
        self.stats.player_last_death_reason = 'killed by %s' % (murderer.name)
        message('You die...', COLOR_ERROR)

    def start_map(self, level):
        from maps.map import Map
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
                if not self.player.is_alive:
                    if self.wizard:
                        if prompt('Die? (Y/N)', [pygame.K_y, pygame.K_n]) == pygame.K_n:
                            new_ui_turn()
                            self.player.resurrect()
                            message('You are resurrected!', COLOR_ERROR)
                            draw_all()
                            continue
                    prompt(
                        'Game over: %s. Press ENTER' % self.stats.player_last_death_reason,
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
                # draw_all()
                pygame.time.delay(DELAY)
        except Quit:
            pass

    def do_walk_command(self, key):
        cmd = decode_walk_key(key)
        if cmd is None:
            return
        new_ui_turn()
        if isinstance(cmd, str):
            getattr(self, 'cmd_' + cmd)()
        else:
            name, args = cmd
            getattr(self, 'cmd_' + name)(*args)
        draw_all()

    def do_command(self, key):
        cmd = decode_interface_key(key)
        if cmd is None:
            return
        new_ui_turn()
        if isinstance(cmd, str):
            getattr(self, 'cmd_' + cmd)()
        else:
            name, args = cmd
            getattr(self, 'cmd_' + name)(*args)
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

    def cmd_perks(self):
        scene = ChoosePerkScene(self.player)
        scene.show()

    def cmd_use_map_object(self):
        from maps.objects import MapObject
        if self.player.tile.obj == None:
            message('Stand on a map object to use.', COLOR_ERROR)
            return
        self.player.tile.obj.on_use(self.player)

    def cmd_ascend(self):
        from maps.tiles import StairUpTile
        if not isinstance(self.player.tile, StairUpTile):
            message('Stand on a up stairway to ascend.', COLOR_ERROR)
            return
        message('You take a moment to rest, and recover your strength.', T.yellow)
        self.player.heal(int(self.player.life.max / 2))
        self.player.mana.fill()
        message('After a rare moment of peace, you ascend higher into the heart of the Temple...', T.yellow)
        self.ascend()

    def cmd_quit(self):
        if prompt('Quit? (Y/N)', [pygame.K_y, pygame.K_n]) == pygame.K_y:
            raise Quit()
        else:
            new_ui_turn()

    def cmd_select(self):
        weapon = self.player.equipment['r']
        if not weapon:
            message('You must hold the bow in your hands.', COLOR_ERROR)
            return
        quiver = self.player.equipment['q']
        if not quiver:
            message('You must carry a quiver.', COLOR_ERROR)
            return
        if quiver.arrows <= 0:
            message('You need ammunition.', COLOR_ERROR)
            return
        mob = look_mode(True)
        if mob:
            self.player.attack(mob)

    def cmd_wizard(self):
        if self.wizard and self.map.level < MAX_DLEVEL:
            self.start_map(self.map.level + 1)

    def cmd_look(self):
        look_mode()

    def cmd_help(self):
        from graphics.scenes.intro_scene import IntroScene
        scene = IntroScene()
        scene.show()

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
            from graphics.scenes.rip_scene import RipScene
            scene = RipScene(self.turns, self.player)
            scene.show()

    def welcome(self):
        message("Brave adventurer, you are now lost in the underground corridors of the Old Temple.", T.yellow)
        message("There is no way to return to your homeland.", T.yellow)
        message("How long can you survive?", T.yellow)


