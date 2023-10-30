from .modifier import Modifier


class AggregateModifier(Modifier):
    def __init__(self, *args):
        self.mods = args

    @property
    def descr(self):
        return sum(mod.descr for mod in self.mods)

    def commit(self, mob):
        for mod in self.mods:
            mod.commit(mob)

    def rollback(self, mob):
        for mod in self.mods:
            mod.rollback(mob)