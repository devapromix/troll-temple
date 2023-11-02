from common.game import Game
from mobs.mobs import *
from mobs.player import *

player = Player(0, FIGHTER)
mob = Bat()

for i in range(50):
    print(Damage.calculate(player, mob))
    # print(Damage.calculate(mob, player))
