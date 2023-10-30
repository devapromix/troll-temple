from common.modifiers.modifier import Modifier


class AddDamage(Modifier):
    def __init__(self, value):
        self.value = value

    @property
    def descr(self):
        return '+%d to damage' % self.value

    def commit(self, mob):
        super().commit(mob)
        mob.damage_bonus += self.value

    def rollback(self, mob):
        super().rollback(mob)
        mob.damage_bonus -= self.value
