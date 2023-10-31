from common.modifiers.modifier import Modifier

class AddConfuse(Modifier):

    @property
    def descr(self):
        return "confuse"

    def commit(self, mob):
        super().commit(mob)
        mob.confused = True

    def rollback(self, mob):
        super().rollback(mob)
        mob.confused = False
