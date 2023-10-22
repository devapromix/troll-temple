from .mob import *

# --- CONSTANTS --- #

FIGHTER = 1
THIEF = 2
RANGER = 3
MAGE = 4

GAME_CLASSES = [["Fighter", FIGHTER, T.light_red],
                ["Thief",   THIEF, T.light_yellow],
                ["Ranger",  RANGER, T.light_green],
                ["Mage",    MAGE, T.light_orange]]

class Player(Mob):
    glyph = '@', T.white
    name = 'Trollhunter'
    hp_regen = 0
    mp_regen = 1
    magic = 0
    radius = 0

    def __init__(self, wizard, selected_game_class):
        super(Player, self).__init__()
        self.game_class = selected_game_class
        self.level = 1
        self.max_hp = 40 - (self.game_class * 5)
        self.hp = self.max_hp
        self.max_mp = self.game_class * 5
        self.mp = self.max_mp
        
        self.has_hp_adv_drop = True
        self.has_mp_adv_drop = False
        
        self.holding_dagger = False        

        self.has_spellbook = False
        self.has_craftbox = False
        self.has_alchemyset = False
        
        self.can_use_dagger = False
        self.can_use_staff = False
        self.can_use_shield = False
        self.can_wear_robe = False

        import items.items as item
        import common.spells as spell
        self.spells = []
        self.effects = []
        self.items = [item.Torch(), item.HealingPotion()]
        if self.game_class == FIGHTER:
            self.hp_regen = 2
            self.mp_regen = 0
            self.magic = 0
            self.radius = 0
            self.can_use_shield = True
            self.items += [item.HealingPotion(), item.ShortSword(), item.RoundShield(), item.LeatherArmor(), item.InstantPoisonPotion()]
        elif self.game_class == THIEF:
            self.hp_regen = 1
            self.mp_regen = 1
            self.magic = 0
            self.radius = 0
            self.has_alchemyset = True
            self.can_use_dagger = True
            self.items += [item.HealingPotion(), item.SmallDagger(), item.LeatherArmor(), item.InstantPoisonPotion()]
        elif self.game_class == RANGER:
            self.hp_regen = 1
            self.mp_regen = 1
            self.magic = 0
            self.radius = 1
            self.has_craftbox = True
            self.items += [item.HealingPotion(), item.HuntingSpear(), item.LeatherArmor()]
        else:
            self.hp_regen = 0
            self.mp_regen = 3
            self.magic = 1
            self.radius = 0
            self.has_hp_adv_drop = False
            self.has_mp_adv_drop = True
            self.has_spellbook = True
            self.can_use_staff = True
            self.can_wear_robe = True # You cannot wear magical armor.
            self.items += [item.ManaPotion(), item.BookHealing(), item.ShortStaff(), item.LeatherArmor()]

        self.equipment = dict((slot, None) for slot in INVENTORY_SLOTS)
        self.speed = 0
        self.fov_range = 3
        self.light_range = 0
        self.action_turns = 1
        self.armor = 0
        self.exp = 0
        self.kills = 0
        self.deaths = 0
        self.death = None
        self.won = False
        self.wizard = wizard

    @property
    def dice(self):
        weapon = self.equipment['w']
        if weapon:
            a, b, c = weapon.dice
        else:
            a, b, c = 1, 3, 0
        return a, b, c

    def max_exp(self):
        return (self.level * 9) + ((self.level - 1) * self.level)

    def add_exp(self, mob):
        self.exp += mob.level
        if self.exp >= self.max_exp():
            self.exp -= self.max_exp()
            self.advance()

    def hp_inc(self):
        if self.game_class == FIGHTER:
            return 4
        elif self.game_class == THIEF:
            return 3
        elif self.game_class == RANGER:
            return 3
        else:
            return 2

    def mp_inc(self):
        if self.game_class == FIGHTER:
            return 1
        elif self.game_class == THIEF:
            return 2
        elif self.game_class == RANGER:
            return 2
        else:
            return 5

    def advance(self):
        self.level += 1
        self.max_hp += self.hp_inc()
        self.hp = self.max_hp
        self.max_mp += self.mp_inc()
        self.mp = self.max_mp

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

    def use_spell(self, spell):
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
        if rand(1, 100) < 95:
            dmg = roll(*self.dice)
            dmg = mon.calc_damage(dmg)
            if dmg > 0:
                if rand(1, 20) < 20:
                    message('You hit the %s (%d).' % (mon.name, dmg))
                else:
                    dmg *= 2
                    message('You critically hit the %s (%d)!' % (mon.name, dmg), COLOR_ALERT)
            mon.damage(dmg)
            if rand(1, 2) == 1 and self.poison > 0:
                mon.poisoned = self.poison
                message('You poisoned the %s (%d)!' % (mon.name, self.poison))
            self.use_energy()
        else:
            message('You miss the %s.' % (mon.name))

    def damage(self, dmg, mon):
        if dmg <= 0:
            message('Your armor protects you.')
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            if not self.death:
                message('You die...', COLOR_ERROR)
                mon.look_normal()
                self.death = 'killed by %s' % (mon.name)

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
        if not self.death:
            super(Player, self).act()
            if self.poisoned > 0:
                message("You are suffering from poison.", COLOR_ERROR)
            self.action_turns += 1
            self.act_effects()

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
        self.deaths += 1
        self.death = None
        self.hp = self.max_hp
        self.mp = self.max_mp

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

    def heal(self, hp):
        self.hp += hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def teleport(self):
        x, y, _ = self.map.random_empty_tile()
        self.move(x, y)

    def has_effect(self, effect):
        for i, ef in enumerate(self.effects):
            if ef[0] == effect:
                return True
        return False

    def add_effect(self, effect, turns):
        if not self.has_effect(effect):
            self.effects.append([effect, turns])
        print(self.effects)

    def act_effects(self):
        pass
