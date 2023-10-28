from .modifier import Modifier


class AddArmor(Modifier):
    def __init__(self, value):
        self.value = value

    @property
    def descr(self):
        return '+%d armor' % (self.value)

    def commit(self, mob):
        mob.armor += self.value

    def rollback(self, mob):
        mob.armor -= self.value

