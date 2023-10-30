from common.modifiers.modifier import Modifier


class Effect:
    modifier = Modifier()
    max_turns = 0

    def __init__(self):
        self.turns = 0
        self.owner = None
        self.__enabled = False

    def register(self, owner):
        self.owner = owner
        self.__start()

    def __start(self):
        assert not self.__enabled
        self.modifier.commit(self.owner)
        self.__enabled = True

    def __finish(self):
        assert self.__enabled
        self.modifier.rollback(self.owner)
        self.__enabled = False

    def act(self):
        if not self.__enabled:
            return

        self.modifier.act(self.owner)
        self.turns += 1
        if self.turns >= self.max_turns:
            self.__finish()


