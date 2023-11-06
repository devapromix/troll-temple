from common.game_class import Game
from mobs.mobs import *
from mobs.player import *

player = Player(0, Classes.FIGHTER)
player.blocking += 200
mob = Bat()

for i in range(50):
    # print(Damage.calculate(player, mob))
    print(Damage.calculate(mob, player))
