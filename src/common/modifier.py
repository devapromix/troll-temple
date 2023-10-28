class Modifier:
    def commit(self, mob):
        raise NotImplementedError("Please, implement this method")

    def rollback(self, mob):
        raise NotImplementedError("Please, implement this method")


class AddMaxHp(Modifier):
    def __init__(self, value):
        self.value = value

    def commit(self, mob):
        mob.max_hp += self.value
        mob.hp += self.value

    def rollback(self, mob):
        mob.max_hp -= self.value
        mob.hp -= self.value