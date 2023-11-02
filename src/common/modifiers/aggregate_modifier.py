from .modifier import Modifier


class AggregateModifier(Modifier):
    def __init__(self, *args):
        self.mods = list(args)

    @property
    def descr(self):
        return ''.join(mod.descr for mod in self.mods)

    def commit(self, mob):
        for mod in self.mods:
            mod.commit(mob)

    def rollback(self, mob):
        for mod in self.mods:
            mod.rollback(mob)

    def __iadd__(self, other):
        if not type(other) is Modifier:
            if isinstance(other, AggregateModifier):
                self.mods.extend(other.mods)
            else:
                self.mods.append(other)
        return self

    def __isub__(self, other):
        self.mods.remove(other)
        return self