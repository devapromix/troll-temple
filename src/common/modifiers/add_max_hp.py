from .modifier import Modifier


class AddMaxHp(Modifier):
    def __init__(self, value):
        self.value = value

    @property
    def descr(self):
        return '+%d maximum life' % (self.value)

    def commit(self, mob):
        mob.life.inc(self.value)

    def rollback(self, mob):
        mob.life.dec(self.value)