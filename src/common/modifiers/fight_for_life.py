from .modifier import Modifier
from ..game import message


class FightForLife(Modifier):
    hp_regen = 5

    @property
    def descr(self):
        return "Regenerate %d twice, if you have less than half" % self.hp_regen

    def act(self, mob):
        if mob.hp <= mob.max_hp // 2:
            # TODO message('You feel a powerful wish to live', COLOR_MAGIC)
            mob.heal(self.hp_regen)
