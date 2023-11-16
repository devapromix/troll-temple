import pygame
import tcod as T

from common.game import init, close, message, COLOR_ERROR, \
    draw_all, prompt, new_ui_turn, Quit, DELAY, decode_walk_key, decode_interface_key, select_item, look_mode, \
    MAX_DLEVEL, select_spell, select_recipe, COLOR_ALERT
from common.stats import Stats
from graphics.scenes.choose_perk_scene import ChoosePerkScene


class Game(object):
    def __init__(self, wizard):
        from mobs.player import Classes
        from graphics.scenes.info_scene import InfoScene
        self.wizard = wizard
        self.wizard = True
        self.selected_game_class = Classes.FIGHTER
        self.keydown = None
        self.stats = Stats()
        self.info_scene = InfoScene()

    def play(self):
        from graphics.scenes.choose_game_class_scene import ChooseGameClassScene
        from graphics.scenes.intro_scene import IntroScene
        from graphics.scenes.title_scene import TitleScene
        init(self)
        TitleScene().show()
        IntroScene().show()
        scene = ChooseGameClassScene(self)
        scene.show()
        self.selected_game_class = scene.selected[1]
        self.start()
        ChoosePerkScene(self.player).show()
        self.info_scene.message("Welcome to the Old Temple!", "Brave adventurer, you are lost in the underground corridors of the Old Temple. It is very dangerous for a lonely traveler here. There is no way to return home. How long can you survive?")
        self.info_scene.show()
        self.loop()
        close()

    def start(self):
        from mobs.player import Player
        from mobs.mobs import TrollKing
        self.player = Player(self.wizard, self.selected_game_class)
        self.player.on_damage += lambda dmg: self.__player_damaged(dmg)
        self.player.on_strike += lambda dmg: self.__player_striked(dmg)
        self.player.on_die += lambda damage: self.player_died(damage.defender, damage.attacker)
        self.final_boss = TrollKing()
        self.final_boss.on_die = self.final_boss_died()
        self.turns = 0
        self.start_map(1)

    def player_died(self, player, murderer):
        self.stats.player_death_count += 1
        self.stats.player_last_death_reason = 'killed by %s' % (murderer.name)
        message('You die...', COLOR_ERROR)

    def final_boss_died(self):
        if prompt('You have defeated the Troll King! Press [ENTER] to continue...', [pygame.K_RETURN]) == pygame.K_RETURN:
            self.info_scene.message("You have defeated True Evil!", "You have come a long way and defeated the terrible tyrant Troll King! Now all the magical power of the Ruby Amulet is in your hands and the White Portal will show you the way home...")
            self.info_scene.show()
            new_ui_turn()

    def start_map(self, level):
        from maps.map import Map
        self.map = Map(level)
        x, y, _ = self.map.random_empty_tile()
        self.player.put(self.map, x, y)

    def ascend(self):
        self.turns += 1
        self.start_map(self.map.level + 1)

    def loop(self):
        from graphics.scenes.rip_scene import RipScene
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
                        'Game over: %s. Press [ENTER] to exit...' % self.stats.player_last_death_reason,
                        [pygame.K_RETURN])
                    scene = RipScene(self.turns, self.player)
                    scene.show()
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

    def cmd_inventory(self):
        from graphics.scenes.inventory_scene import InventoryScene
        scene = InventoryScene(self.player)
        scene.show()

    def cmd_use_map_object(self):
        from maps.objects import MapObject
        if self.player.tile.obj == None:
            message('Stand on a map object to use.', COLOR_ERROR)
            return
        self.player.tile.obj.on_use(self.player)

    def cmd_ascend(self):
        from maps.tiles import StairUpTile
        if not self.wizard and not isinstance(self.player.tile, StairUpTile):
            message('Stand on a up stairway to ascend.', COLOR_ERROR)
            return
        self.player.heal(int(self.player.life.max / 2))
        self.player.mana.fill()
        self.info_scene.message("You rise higher and higher in the heart of the mountain...", "You take a moment to rest, and recover your strength... After a rare moment of peace, you ascend higher into the heart of the Old Temple...")
        self.info_scene.show()
        self.ascend()

    def cmd_quit(self):
        from graphics.scenes.rip_scene import RipScene
        if prompt('Quit? (Y/N)', [pygame.K_y, pygame.K_n]) == pygame.K_y:
            scene = RipScene(self.turns, self.player)
            scene.show()
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
        if self.wizard:
            self.cmd_ascend()

    def cmd_look(self):
        look_mode()

    def cmd_help(self):
        from graphics.scenes.intro_scene import IntroScene
        scene = IntroScene()
        scene.show()
        
    def cmd_finditem(self):
        from mobs.player import Classes
        from items.corpse import Corpse
        from mobs.drop import AdvDrop
        from common.utils import rand
        if self.player.game_class != Classes.FIGHTER:
            message("Only a fighter can use this ability!", COLOR_ERROR)
            return
        tile = self.player.tile
        if tile.items == []:
            message('There is no corpse here to examine.', COLOR_ERROR)
        else:
            for item in tile.items:
                if isinstance(item, Corpse):
                    tile.items.remove(item)
                    if rand(1, 4) == 1:
                        d = AdvDrop(self.player)
                        d.drop()
                        message("You found something.")
                    else:
                        message("You didn't find anything.")
                    self.player.use_energy()
        
    def cmd_conjure_mana_orb(self):
        from mobs.player import Classes
        from items.mana_orb import ManaOrb
        if self.player.game_class != Classes.MAGE:
            message("Only a mage can use this ability!", COLOR_ERROR)
            return
        self.need_mana = 15
        if self.player.mana.cur < self.need_mana:
            message('Need more mana!', COLOR_ERROR)
            return
        message('You have conjure a mana orb.')
        self.player.mana.modify(-self.need_mana)
        self.player.tile.items.append(ManaOrb())
        
    def cmd_invisibility(self):
        from mobs.player import Invisibility, Classes
        if self.player.game_class != Classes.THIEF:
            message("Only a thief can use this ability!", COLOR_ERROR)
            return
        if self.player.invisibility == Invisibility.NONE:
            self.player.invisibility = Invisibility.SHADOW
            message("You hide in the shadows!")
        else:
            self.player.visibility()

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

    def cmd_alchemyset(self):
        if self.player.has_alchemyset:
            recipe = select_recipe('Select a recipe to craft, ESC to exit', self.player.recipes)
            if recipe:
                self.player.craft(recipe)
        else:
            message("You don't have an alchemyset!", COLOR_ERROR)

    def cmd_character(self):
        from graphics.scenes.character_scene import CharacterScene
        scene = CharacterScene(self.turns, self.player)
        scene.show()

    def cmd_test(self):
        if self.wizard:
            from graphics.scenes.inventory_scene import InventoryScene
            scene = InventoryScene(self.player)
            scene.show()

    def __player_damaged(self, damage):
        name = damage.attacker.name
        if damage.status == damage.status.NORMAL:
            message('The %s hits you (%d).' % (name, int(damage)))
        elif damage.status == damage.status.CRITICAL:
            message('The %s critically hits you (%d)!' % (name, int(damage)), COLOR_ALERT)
        elif damage.status == damage.status.EVADED:
            message('The %s misses you.' % name)
        elif damage.status == damage.status.BLOCKED:
            message("You block the attack.")
        elif damage.status == damage.status.ABSORBED:
            message('Your armor protects you.')

    def __player_striked(self, damage):
        mon = damage.defender
        if damage.status == damage.status.NORMAL:
            message('You hit the %s (%d).' % (mon.name, int(damage)))
        elif damage.status == damage.status.CRITICAL:
            message('You critically hit the %s (%d)!' % (mon.name, int(damage)), COLOR_ALERT)
        elif damage.status == damage.status.EVADED:
            message('You miss the %s.' % mon.name)
        elif damage.status == damage.status.BLOCKED:
            message('Monster have blocked your strike')
        elif damage.status == damage.status.ABSORBED:
            message('Monster have too powerful armor')


