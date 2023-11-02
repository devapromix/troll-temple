from common.modifiers.modifier import Modifier


class AddMaxMana(Modifier):
    def __init__(self, value):
        self.value = value

    @property
    def descr(self):
        return "+%s mana" % self.value

    def commit(self, mob):
        super().commit(mob)
        mob.mana.inc(self.value)

    def rollback(self, mob):
        super().rollback(mob)
        mob.mana.dec(self.value)
