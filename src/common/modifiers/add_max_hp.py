from .modifier import Modifier


class AddMaxHp(Modifier):
    def __init__(self, value):
        self.value = value

    @property
    def descr(self):
        return '+%d maximum hp' % (self.value)

    def commit(self, mob):
        mob.max_hp += self.value
        mob.hp += self.value

    def rollback(self, mob):
        mob.max_hp -= self.value
        mob.hp -= self.value