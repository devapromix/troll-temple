from .modifier import Modifier


class Mod(Modifier):
    def __init__(self, attr_name, value):
        self.attr_name = attr_name
        self.value = value

    @property
    def descr(self):
        return ' %s%d %s' % ('+' if self.value > 0 else '', self.value, self.attr_name)

    def commit(self, mob):
        setattr(mob, self.attr_name, getattr(mob, self.attr_name) + self.value)

    def rollback(self, mob):
        setattr(mob, self.attr_name, getattr(mob, self.attr_name) - self.value)
