import pygame
from .monster import *

class FlyMonster(Monster):
    ABSTRACT = True
    fears_light = True
    drop_rate = 10

class UndeadMonster(Monster):
    ABSTRACT = True
    drop_rate = 10

class GhostMonster(UndeadMonster):
    ABSTRACT = True
    fears_light = True
    enters_walls = True
    drop_rate = 10

class MageMonster(Monster):
    ABSTRACT = True
    mana_regen = 10
    magic = 5
    fov_range = 10
    drop_rate = 20

class RareMonster(Monster):
    ABSTRACT = True
    life_regen = 5
    drop_rate = 30
    rarity = 15

class Dragon(RareMonster):
    ABSTRACT = True
    life_regen = 25
    mana_regen = 10
    fov_range = 7
    drop_rate = 30
    has_skin = True

class RareDragon(Dragon):
    ABSTRACT = True
    life_regen = 30
    rarity = 25

class BossMonster(Monster):
    ABSTRACT = True
    life_regen = 15
    fov_range = 7
    drop_rate = 30

class FinalBossMonster(BossMonster):
    ABSTRACT = True
    life_regen = 20
    fov_range = 8
    drop_rate = 30

# --- MONSTERS #1 --- #

class Rat(Monster):
    name = 'rat'
    glyph = 'r', T.light_gray
    has_skin = True
    life = 4
    dice = 1, 2, 0
    multi = 4
    level = 1
    dungeons = 1, 2
    rarity = 1

class Bat(FlyMonster):
    name = 'bat'
    glyph = 'b', T.darker_orange
    has_skin = True
    life = 6
    speed = 3
    dice = 1, 2, 0
    multi = 3
    level = 1
    dungeons = 1, 3
    rarity = 1
    evasion = 70

class Crawler(Monster):
    name = 'crawler'
    glyph = 'c', T.lighter_blue
    life = 5
    dice = 1, 2, 0
    multi = 3
    level = 1
    dungeons = 1, 2
    rarity = 1

class GiantAnt(Monster):
    name = 'giant ant'
    glyph = 'a', T.orange
    life = 4
    dice = 1, 2, 0
    multi = 4
    level = 1
    dungeons = 1, 2
    rarity = 1

# --- MONSTERS #2 --- #

class GiantSpider(Monster):
    name = 'giant spider'
    glyph = 's', T.light_gray
    life = 8
    speed = 1
    dice = 1, 3, 0
    poison = 4
    armor = 0
    multi = 3
    level = 2
    dungeons = 2, 3
    rarity = 1

class Kobold(Monster):
    name = 'kobold'
    glyph = 'k', T.light_green
    has_skin = True
    life = 10
    dice = 1, 3, 1
    speed = 1
    armor = 0
    multi = 3
    level = 2
    dungeons = 2, 3
    rarity = 1

class Lizard(Monster):
    name = 'lizard'
    glyph = 'l', T.light_blue
    has_skin = True
    life = 9
    dice = 1, 3, 0
    poison = 3
    armor = 1
    multi = 3
    level = 2
    dungeons = 2, 3
    rarity = 1

class Viper(Monster):
    name = 'viper'
    glyph = 'v', T.light_green
    has_skin = True
    life = 7
    dice = 1, 3, 0
    poison = 7
    multi = 4
    level = 2
    dungeons = 2, 3
    rarity = 1

# --- MONSTERS #3 --- #

class BlackKobold(Monster):
    name = 'black kobold'
    glyph = 'k', T.gray
    has_skin = True
    life = 12
    dice = 1, 3, 1
    armor = 0
    level = 3
    dungeons = 3, 4
    rarity = 1

class Scorpion(Monster):
    name = 'scorpion'
    glyph = 's', T.orange
    life = 15
    dice = 1, 3, 0
    poison = 6
    level = 3
    dungeons = 3, 4
    rarity = 1

class Bloodfly(FlyMonster):
    name = 'bloodfly'
    glyph = 'b', T.gray
    life = 16
    dice = 1, 3, 0
    poison = 5
    armor = 1
    level = 3
    dungeons = 3, 4
    rarity = 1

class Goblin(Monster):
    name = 'goblin'
    glyph = 'g', T.light_blue
    has_skin = True
    life = 14
    dice = 1, 3, 2
    armor = 1
    level = 3
    dungeons = 3, 4
    rarity = 1

class Hobgoblin(Monster):
    name = 'hobgoblin'
    glyph = 'h', T.light_green
    has_skin = True
    life = 15
    dice = 1, 4, 2
    armor = 1
    level = 3
    dungeons = 3, 4
    rarity = 1

# --- MONSTERS #4 --- #

class DarkGoblin(Monster):
    name = 'dark goblin'
    glyph = 'g', T.grey
    has_skin = True
    life = 18
    dice = 2, 3, 0
    armor = 1
    level = 4
    dungeons = 4, 5
    rarity = 1

class LowOrc(Monster):
    name = 'low orc'
    glyph = 'o', T.red
    has_skin = True
    life = 20
    dice = 2, 3, 1
    armor = 2
    level = 4
    dungeons = 4, 5
    rarity = 1

class DustElemental(MageMonster):
    name = 'dust elemental'
    glyph = 'e', T.green
    life = 15
    dice = 2, 3, 0
    level = 4
    dungeons = 4, 5
    rarity = 1

class CrystalSpider(Monster):
    name = 'crystal spider'
    glyph = 's', T.light_cyan
    life = 19
    dice = 2, 3, 1
    poison = 7
    armor = 1
    level = 4
    multi = 2
    dungeons = 4, 5
    rarity = 1

# --- MONSTERS #5 --- #

class Scavenger(GhostMonster):
    name = 'scavenger'
    glyph = 's', T.light_green
    life = 25
    dice = 2, 3, 2
    level = 5    
    armor = 2
    dungeons = 5, 6
    rarity = 1

class Ghost(GhostMonster):
    name = 'ghost'
    glyph = 'g', T.white
    life = 24
    speed = 1
    dice = 2, 4, 0
    level = 5    
    multi = 2
    dungeons = 5, 6
    rarity = 1

class KillerBat(FlyMonster):
    name = 'killer bat'
    glyph = 'b', T.darker_orange
    has_skin = True
    life = 22
    speed = 3
    dice = 3, 3, 0
    multi = 3
    level = 5
    dungeons = 5, 7
    rarity = 1

class BearMan(Monster):
    name = 'bear man'
    glyph = 'b', T.dark_orange
    has_skin = True
    life = 25
    dice = 2, 4, 1
    armor = 2
    level = 4
    dungeons = 5, 6
    rarity = 1

# --- MONSTERS #6 --- #

class RockRat(Monster):
    name = 'rock rat'
    glyph = 'r', T.light_gray
    has_skin = True
    life = 28
    dice = 2, 5, 0
    multi = 3
    level = 6
    dungeons = 6, 8
    rarity = 1

class Snapper(Monster):
    name = 'snapper'
    glyph = 's', T.lighter_green
    has_skin = True
    life = 32
    poison = 9
    dice = 2, 4, 1
    level = 6
    dungeons = 6, 8
    rarity = 1

class HillGiant(RareMonster):
    name = 'hill giant'
    glyph = 'G', T.gray
    has_skin = True
    life = 28
    dice = 2, 5, 1
    level = 6    
    armor = 4
    dungeons = 6, 7

class Troll(RareMonster):
    name = 'troll'
    glyph = 'T', T.light_blue
    has_skin = True
    life = 30
    dice = 2, 5, 2
    level = 6    
    armor = 5
    dungeons = 6, 7

# --- MONSTERS #7 --- #

class FlyingEye(FlyMonster):
    name = 'flying eye'
    glyph = 'e', T.light_blue
    life = 32
    dice = 2, 5, 0
    multi = 3
    level = 7
    dungeons = 7, 7
    rarity = 1

class FireSkeleton(UndeadMonster):
    name = 'fire skeleton'
    glyph = 's', T.light_red
    life = 35
    dice = 2, 5, 2
    multi = 2
    level = 7
    dungeons = 7, 8
    rarity = 1

class StoneShark(Monster):
    name = 'stoneshark'
    glyph = 's', T.light_grey
    life = 35
    dice = 2, 6, 0
    armor = 2
    level = 7
    dungeons = 7, 8
    rarity = 1

class Vampire(RareMonster):
    name = 'vampire'
    glyph = 'V', T.grey
    life = 32
    dice = 2, 5, 2
    armor = 3
    level = 7
    dungeons = 7, 9
    rarity = 10

class Ogre(RareMonster):
    name = 'ogre'
    glyph = 'O', T.light_green
    has_skin = True
    life = 40
    dice = 2, 6, 2
    armor = 7
    level = 7    
    dungeons = 7, 8

# --- MONSTERS #8 --- #

class Skeleton(UndeadMonster):
    name = 'skeleton'
    glyph = 's', T.light_grey
    life = 37
    dice = 2, 5, 3
    multi = 2
    level = 8    
    dungeons = 8, 8
    rarity = 1

class Zombie(UndeadMonster):
    name = 'zombie'
    glyph = 'z', T.light_green
    life = 38
    dice = 2, 6, 1
    level = 8    
    dungeons = 8, 8
    rarity = 1

class BoneGolem(UndeadMonster):
    name = 'bone golem'
    glyph = 'G', T.light_grey
    life = 42
    armor = 7
    dice = 3, 4, 3
    level = 8    
    dungeons = 8, 9
    rarity = 15

class Necromancer(MageMonster):
    name = 'necromancer'
    glyph = 'n', T.light_grey
    life = 40
    dice = 3, 4, 2
    summoner = True
    magic = 9
    level = 8    
    dungeons = 8, 8
    rarity = 5

# --- MONSTERS #9 --- #

class MaddeningEye(FlyMonster):
    name = 'maddening eye'
    glyph = 'e', T.yellow
    life = 44
    dice = 3, 5, 0
    armor = 1
    level = 9    
    dungeons = 9, 10
    rarity = 1

class Shadowbeast(UndeadMonster):
    name = 'shadowbeast'
    glyph = 's', T.light_grey
    has_skin = True
    life = 44
    dice = 2, 5, 5
    armor = 2
    poison = 12
    level = 9    
    dungeons = 8, 10
    rarity = 1

class StoneGolem(RareMonster):
    name = 'stone golem'
    glyph = 'G', T.light_grey
    life = 44
    armor = 10
    dice = 3, 5, 2
    level = 9    
    dungeons = 9, 10

class FireGolem(RareMonster):
    name = 'fire golem'
    glyph = 'G', T.light_red
    life = 46
    armor = 10
    dice = 3, 5, 2
    level = 9    
    dungeons = 9, 10

# --- MONSTERS #10 --- #

class RockRaider(Monster):
    name = 'rock raider'
    glyph = 'r', T.light_grey
    has_skin = True
    life = 48
    poison = 15
    armor = 4
    dice = 2, 7, 2
    level = 10    
    dungeons = 10, 11
    rarity = 1

class DustDevil(Monster):
    name = 'dust devil'
    glyph = 'd', T.yellow
    has_skin = True
    life = 52
    dice = 2, 8, 1
    armor = 7
    level = 10    
    dungeons = 10, 11
    rarity = 1

class SpikedDevil(Monster):
    name = 'spiked devil'
    glyph = 'd', T.grey
    has_skin = True
    life = 54
    dice = 2, 8, 1
    armor = 6
    level = 10    
    dungeons = 10, 11
    rarity = 1

class Wraith(GhostMonster):
    name = 'wraith'
    glyph = 'w', T.light_grey
    life = 50
    dice = 3, 5, 2
    level = 10
    dungeons = 10, 11
    rarity = 1

# --- MONSTERS #11 --- #

class Drake(Monster):
    name = 'drake'
    glyph = 'd', T.light_green
    has_skin = True
    life = 55
    dice = 2, 9, 0
    armor = 3
    level = 11    
    dungeons = 11, 12
    rarity = 1

class Spectre(GhostMonster):
    name = 'spectre'
    glyph = 's', T.light_grey
    life = 54
    speed = 1
    dice = 3, 6, 0
    multi = 3
    level = 11    
    dungeons = 11, 12
    rarity = 1

class Wyrm(Monster):
    name = 'wyrm'
    glyph = 'w', T.light_grey
    has_skin = True
    life = 56
    dice = 3, 6, 1
    poison = 20
    armor = 5
    level = 11    
    dungeons = 11, 12
    rarity = 1

class ColossalHydra(RareMonster):
    name = 'colossal hydra'
    glyph = 'H', T.dark_green
    has_skin = True
    life = 58
    poison = 25
    armor = 12
    dice = 4, 4, 4
    level = 11    
    dungeons = 11, 12

# --- MONSTERS #12 --- #

class SoulSucker(FlyMonster):
    name = 'soul sucker'
    glyph = 's', T.light_blue
    life = 60
    dice = 3, 7, 0
    armor = 4
    multi = 3
    level = 12    
    dungeons = 12, 12
    rarity = 1

class HugeSpider(Monster):
    name = 'huge spider'
    glyph = 's', T.light_grey
    life = 60
    dice = 3, 6, 3
    poison = 22
    armor = 8
    level = 12    
    dungeons = 12, 12
    rarity = 1

class Manticore(RareMonster):
    name = 'manticore'
    glyph = 'M', T.light_red
    has_skin = True
    life = 65
    dice = 3, 6, 2
    armor = 10
    level = 12    
    dungeons = 12, 12

class Summoner(MageMonster):
    name = 'summoner'
    glyph = 's', T.light_blue
    life = 60
    dice = 3, 6, 2
    summoner = True
    magic = 12
    multi = 3
    armor = 5
    level = 12    
    dungeons = 12, 12
    rarity = 5

# --- DRAGONS --- #

class WhiteDragon(Dragon):
    name = 'white dragon'
    glyph = 'D', T.white
    life = 85
    dice = 3, 6, 1
    armor = 12
    level = 12    
    dungeons = 12, 12

class BlueDragon(Dragon):
    name = 'blue dragon'
    glyph = 'D', T.light_blue
    life = 90
    dice = 3, 5, 3
    armor = 5
    level = 12    
    dungeons = 12, 12

class GreenDragon(Dragon):
    name = 'green dragon'
    glyph = 'D', T.light_green
    life = 75
    dice = 3, 5, 3
    poison = 25
    armor = 7
    level = 12    
    dungeons = 12, 12

class RedDragon(Dragon):
    name = 'red dragon'
    glyph = 'D', T.light_red
    life = 70
    dice = 3, 6, 4
    armor = 8
    level = 12    
    dungeons = 12, 12

class GoldDragon(Dragon):
    name = 'gold dragon'
    glyph = 'D', T.gold
    life = 80
    dice = 3, 6, 2
    armor = 10
    level = 12    
    dungeons = 12, 12

class AncientBlackDragon(RareDragon):
    name = 'ancient black dragon'
    glyph = 'D', T.dark_grey
    life = 100
    dice = 3, 7, 1
    armor = 15
    level = 12    
    dungeons = 12, 12

# --- BOSSES --- #

class FireGoblin(BossMonster):
    ABSTRACT = True
    name = 'fire goblin'
    glyph = 'G', T.light_red
    has_skin = True
    life = 20
    dice = 1, 4, 3
    armor = 2
    level = 3
    dungeons = 3, 3

    def die(self, dmg):
        super().die(dmg)
        self.tile.items.append(ScrollRedPortal())
        self.adv_drop()
        self.rare_drop()
        
class Werewolf(BossMonster):
    ABSTRACT = True
    name = 'werewolf'
    glyph = 'W', T.light_grey
    has_skin = True
    life = 40
    dice = 2, 5, 4
    level = 6    
    armor = 5
    dungeons = 6, 6

    def die(self, dmg):
        super().die(dmg)
        self.tile.items.append(ScrollGreenPortal())
        self.adv_drop()
        self.rare_drop()
        
class Abomination(BossMonster):
    ABSTRACT = True
    name = 'abomination'
    glyph = 'A', T.light_blue
    life = 60
    dice = 2, 7, 5
    armor = 8
    poison = 20
    level = 9    
    dungeons = 9, 9

    def die(self, dmg):
        super().die(dmg)
        self.tile.items.append(ScrollBluePortal())
        self.adv_drop()
        self.rare_drop()
        
# --- FINAL BOSS --- #

class TrollKing(FinalBossMonster):
    ABSTRACT = True
    name = 'troll king'
    glyph = 'T', T.red
    has_skin = True
    life = 75
    dice = 4, 6, 5
    armor = 10
    level = 12
    dungeons = 12, 12

    def __init__(self):
        super().__init__()

    def die(self, dmg):
        from items.amulets import RubyAmulet
        super().die(dmg)
        self.tile.items.append(ScrollWhitePortal())
        self.tile.items.append(RubyAmulet())
        self.adv_drop()
        self.rare_drop()
        self.unique_drop()
        
