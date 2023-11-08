from .modifier import Modifier


class AggregateModifier(Modifier):
    def __init__(self, *args):
        self.mods = list(args)

    @property
    def descr(self):
        return ' '.join(mod.descr for mod in self.mods)

    def commit(self, mob):
        for mod in self.mods:
            mod.commit(mob)

    def rollback(self, mob):
        for mod in self.mods:
            mod.rollback(mob)

    def __iadd__(self, other):
        if not type(other) is Modifier:
            if isinstance(other, AggregateModifier):
                for mod in other:
                    self.__add(mod)
            else:
                self.__add(other)
        return self

    def __len__(self): return len(self.mods)
    def __iter__(self): return self.mods.__iter__()
    #def __next__(self): return self.mods.__next__()

    def __add(self, new_mod):
        for mod in self.mods:
            if mod.try_union(new_mod):
                return
        self.mods.append(new_mod)


    def __isub__(self, other):
        self.mods.remove(other)
        return self