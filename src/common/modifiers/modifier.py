
# Describe a change of attribute inside mob.
# It is atomic (the smallest part). It can do rollback.
# Example: +10 armor, +1% critical chance
class Modifier:
    @property
    def descr(self):
        return ''

    def __str__(self):
        return self.descr

    def commit(self, mob):
        pass

    def rollback(self, mob):
        pass

    def act(self, mob):
        pass

    def try_union(self, other):
        return type(self) is type(other)

    def __iadd__(self, other):
        if type(self) is Modifier:
            return other
        from common.modifiers.aggregate_modifier import AggregateModifier
        if isinstance(other, AggregateModifier):
            other += self
            return other
        else:
            return AggregateModifier(self, other)
