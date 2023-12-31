from .modifier import Modifier
from ..game import message


class FightForLife(Modifier):
    life_regen = 5

    @property
    def descr(self):
        return "Regenerate %d twice, if you have less than half" % self.life_regen

    def act(self, mob):
        if mob.life.cur <= mob.life.max // 2:
            # TODO message('You feel a powerful wish to live', COLOR_MAGIC)
            mob.heal(self.life_regen)
