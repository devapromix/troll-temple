from .modifier import Modifier

class DamageMod(Modifier):

    def __init__(self, value):
        self.value = value
        
    @property
    def descr(self):
        return '+%d damage' % self.value
        
    def commit(self, mob):
        super().commit(mob)
        a, b, c = mob.dice
        c += self.value
        mob.dice = a, b, c
        
    def rollback(self, mob):
        super().rollback(mob)
        a, b, c = mob.dice
        c -= self.value
        mob.dice = a, b, c
