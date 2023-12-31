from .damage import *
from .mob import *
from .perks.perks_container import PerksContainer


# --- CONSTANTS --- #

class Invisibility(Enum):
    FULL = 0
    SHADOW = 1
    NONE = 2

class Classes(Enum):
    FIGHTER = 1
    THIEF = 2
    RANGER = 3
    MAGE = 4


GAME_CLASSES = [["FIGHTER", Classes.FIGHTER, T.light_red, "heroic_sword"],
                ["THIEF", Classes.THIEF, T.light_yellow, "blood_dagger"],
                ["RANGER", Classes.RANGER, T.light_green, "hunter_bow"],
                ["MAGE", Classes.MAGE, T.lighter_blue, "wonder_staff"]]


class Player(Mob):
    glyph = '@', T.white
    name = 'Trollhunter'
    life_regen = 0
    mana_regen = 1
    radius = 0

    def __init__(self, wizard, game_class: Classes):
        super(Player, self).__init__()
        self.game_class = game_class
        self.level = 1
        self.life.max = 40 - (self.game_class.value * 5)
        self.life.fill()
        self.mana.max = self.game_class.value * 5
        self.mana.fill()
        self.perks = PerksContainer(self)

        self.has_life_adv_drop = True
        self.has_mana_adv_drop = False

        self.holding_dagger = False
        self.holding_bow = False
        self.holding_quiver = False

        self.has_spellbook = False
        self.has_craftbox = False
        self.has_alchemyset = False

        self.can_use_lockpick = False

        self.can_use_dagger = False
        self.can_use_staff = False
        self.can_use_shield = False
        self.can_use_bow = False

        self.can_wear_cloth_armor = False
        self.can_wear_leather_armor = False
        self.can_wear_mail_armor = False

        import items.items as item
        import common.spells as spell
        from items.light_sources import Torch
        from items.amulets import RavenAmulet, WispAmulet, WardAmulet
        self.spells = []
        self.recipes = []
        self.plans = []
        self.items = [Torch(), item.HealingPotion()]
        if self.game_class == Classes.FIGHTER:
            self.life_regen = 2
            self.mana_regen = 0
            self.radius = 0
            self.can_use_shield = True
            self.can_wear_leather_armor = True
            self.can_wear_mail_armor = True
            self.items += [item.HealingPotion(), item.ShortSword(), item.RoundShield(), item.RingMail()]
            self.items += [RavenAmulet(), WispAmulet(), WardAmulet()]
        elif self.game_class == Classes.THIEF:
            self.life_regen = 1
            self.mana_regen = 1
            self.radius = 0
            self.has_alchemyset = True
            self.can_use_dagger = True
            self.can_use_lockpick = True
            self.can_wear_leather_armor = True
            self.items += [item.HealingPotion(), item.SmallDagger(), item.ShadowArmor(), item.InstantPoisonPotion()]
        elif self.game_class == Classes.RANGER:
            self.life_regen = 1
            self.mana_regen = 1
            self.radius = 1
            self.has_craftbox = True
            self.can_use_bow = True
            self.can_wear_leather_armor = True
            self.items += [item.HealingPotion(), item.HunterBow(), item.LightQuiver(), item.QuiltedArmor()]
        else:
            self.life_regen = 0
            self.mana_regen = 3
            self.magic = 1
            self.radius = 0
            self.has_life_adv_drop = False
            self.has_mana_adv_drop = True
            self.has_spellbook = True
            self.can_use_staff = True
            self.can_wear_cloth_armor = True
            self.items += [item.ManaPotion(), item.BookHealing(), item.ShortStaff(), item.CultistRobe()]

        self.equipment = dict((slot, None) for slot in INVENTORY_SLOTS)
        self.speed = 0
        self.bonus_damage = 0
        self.fov_range = 3
        self.light_range = 0
        self.action_turns = 1
        self.invisibility = Invisibility.NONE
        self.armor = 0
        self.exp = 0
        self.kills = 0
        self.wizard = wizard

    @property
    def dice(self):
        weapon = self.equipment['w']
        if weapon:
            a, b, c = weapon.dice
        else:
            a, b, c = 1, 3, 0
        return a, b, self.bonus_damage + c

    def max_exp(self):
        return (self.level * 9) + ((self.level - 1) * self.level)

    def add_exp(self, mob):
        self.exp += mob.level
        if self.exp >= self.max_exp():
            self.exp -= self.max_exp()
            self.advance()

    def _life_inc(self):
        if self.game_class == Classes.FIGHTER:
            return 4
        elif self.game_class == Classes.THIEF:
            return 3
        elif self.game_class == Classes.RANGER:
            return 3
        else:
            return 2

    def _mana_inc(self):
        if self.game_class == Classes.FIGHTER:
            return 1
        elif self.game_class == Classes.THIEF:
            return 2
        elif self.game_class == Classes.RANGER:
            return 2
        else:
            return self.magic + 5

    def advance(self):
        self.level += 1
        self.life.inc(self._life_inc())
        self.life.fill()
        self.mana.inc(self._mana_inc())
        self.mana.fill()

        from graphics.scenes.choose_perk_scene import ChoosePerkScene
        ChoosePerkScene(self).show()

        message('Congratulations! You advance to level %d.' % self.level,
                COLOR_ALERT)

    def change_light_range(self, n):
        self.light_range += n
        self.fov_range += n
        self.map.recalc_fov()

    def has_equipped(self, item):
        return item.slot and self.equipment[item.slot] == item

    def put(self, m, x, y):
        super(Player, self).put(m, x, y)
        self.map.player = self
        self.map.recalc_fov()

    def move(self, x, y):
        super(Player, self).move(x, y)
        self.map.recalc_fov()
        self.tile.on_enter()
        if self.tile.obj != None:
            self.tile.obj.on_enter()
        if self.tile.items:
            if len(self.tile.items) == 1:
                message('You see here %s.' % self.tile.items[0].a)
            else:
                message('Several items are lying here.')
        self.use_energy()

    def walk(self, dx, dy):
        if dx == 0 and dy == 0:
            self.wait()
            return
        destx, desty = self.x + dx, self.y + dy
        if not self.map.in_map(destx, desty):
            return False
        tile = self.map.tiles[destx][desty]
        if tile.mob:
            self.attack(tile.mob)
        elif not tile.walkable and not self.wizard:
            pass
        else:
            self.move(destx, desty)

    def use(self, item):
        if item.slot is None:
            item.on_use(self)
            self.use_energy()
        elif self.has_equipped(item):
            self.unequip(item)
        else:
            self.equip(item)

    def cast(self, spell):
        if spell.on_use(self):
            self.use_energy()

    def unequip(self, item):
        message('You unequip the %s.' % item.descr)
        item.on_unequip(self)
        self.equipment[item.slot] = None
        self.use_energy()

    def equip(self, item):
        old_item = self.equipment[item.slot]
        if item.on_equip(self):
            if old_item:
                self.unequip(old_item)
            message('You equip the %s.' % item.descr)
            self.equipment[item.slot] = item
            self.use_energy()

    def attack(self, mon):
        super().attack(mon)
        self.use_energy()
        self.visibility()

    def die(self, damage):
        super().die(damage)
        damage.attacker.look_normal()

    def pick_up(self, item):
        if len(self.items) == INV_SIZE:
            message('You can\'t carry anymore items.', COLOR_ERROR)
            return
        assert item in self.tile.items
        self.tile.items.remove(item)
        self.items.append(item)
        message('You pick up the %s.' % item.descr)
        self.use_energy()

    def drop(self, item):
        if self.has_equipped(item):
            self.unequip(item)
        self.items.remove(item)
        self.tile.items.append(item)
        message('You drop the %s.' % item.descr)
        self.use_energy()

    def act(self):
        if self.is_alive:
            super(Player, self).act()
            if self.poisoned > 0:
                message("You are suffering from poison.", COLOR_ERROR)
            self.action_turns += 1

    def use_energy(self):
        self.action_turns -= 1

    def wait(self):
        self.use_energy()

    def extinguish(self, light):
        message('Your %s is extinguished!' % light.descr)
        light.on_unequip(self)
        self.equipment['l'] = None
        self.items.remove(light)

    def heartbeat(self):
        super(Player, self).heartbeat()
        light = self.equipment['l']
        if light:
            light.turns_left -= 1
            if light.turns_left <= 0:
                self.extinguish(light)

    def resurrect(self):
        assert not self.is_alive
        self.is_alive = True
        self.life.fill()
        self.mana.fill()

    def has_spell(self, spell_type):
        for i, spell in enumerate(self.spells):
            if isinstance(spell, spell_type):
                return True
        return False

    def try_learn_spell(self, spell):
        if self.has_spellbook:
            if not self.has_spell(spell):
                self.spells.append(spell())
                message("You've learned a new spell!", COLOR_MAGIC)
                return True
            else:
                message("You already know this spell!", COLOR_ERROR)
                return False
        else:
            message("You don't have a spellbook!", COLOR_ERROR)
            return False

    def heal(self, life):
        self.life.modify(life)

    def teleport(self):
        x, y, _ = self.map.random_empty_tile()
        self.move(x, y)
        
    def visibility(self):
        if self.invisibility != Invisibility.NONE:
            self.invisibility = Invisibility.NONE
            message("You come out of the shadows!")
        

    def create(self, recipe):
        pass


    def craft(self, plan):
        pass
        
