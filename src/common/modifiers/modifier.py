# Describe a change of attribute inside mob.
# It is atomic (the smallest part). It can do rollback.
# Example: +10 armor, +1% critical chance
class Modifier:
    @property
    def descr(self):
        raise NotImplementedError("Please, implement this method")

    def commit(self, mob):
        pass

    def rollback(self, mob):
        pass

    def act(self, mob):
        pass
