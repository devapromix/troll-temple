from .modifier import Modifier


class AttribMod(Modifier):
    DESCRIPTIONS = {
        'life': '+%d life',
        'mana': '+%d mana'
    }

    def __init__(self, attr_name, value):
        self.attr_name = attr_name
        self.value = value

    @property
    def descr(self):
        return self.DESCRIPTIONS[self.attr_name] % self.value

    def try_union(self, other):
        if super().try_union(other):
            if self.attr_name == other.attr_name:
                self.value += other.value
                return True
        return False

    def commit(self, mob):
        super().commit(mob)
        attribute = getattr(mob, self.attr_name)
        attribute.inc(self.value)

    def rollback(self, mob):
        super().rollback(mob)
        attribute = getattr(mob, self.attr_name)
        attribute.dec(self.value)


class AddMaxLife(AttribMod):

    def __init__(self, value): super().__init__('life', value)


class AddMaxMana(AttribMod):

    def __init__(self, value): super().__init__('mana', value)
