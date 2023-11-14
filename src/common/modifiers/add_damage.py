from .modifier import Modifier

class DamageMod(Modifier):

    def __init__(self, value):
        self.value = value
        
    @property
    def descr(self):
        return '+%d damage' % self.value
        
    def commit(self, mob):
        super().commit(mob)
        mob.bonus_damage += self.value
        
    def rollback(self, mob):
        super().rollback(mob)
        mob.bonus_damage -= self.value
