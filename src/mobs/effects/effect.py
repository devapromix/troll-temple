from common.modifiers.modifier import Modifier


class Effect:
    modifier = Modifier()
    max_turns = 0

    def __init__(self):
        self.turns = 0
        self.owner = None
        self.__on_finish = None
        self.__enabled = False

    def register(self, owner, on_finish = None):
        self.owner = owner
        self.__on_finish = on_finish
        self.__start()

    def __start(self):
        assert not self.__enabled
        self.modifier.commit(self.owner)
        self.__enabled = True

    def __finish(self):
        assert self.__enabled
        self.modifier.rollback(self.owner)
        self.__enabled = False
        if self.__on_finish is not None:
            self.__on_finish(self)

    def act(self):
        if not self.__enabled:
            return

        self.modifier.act(self.owner)
        self.turns += 1
        if self.turns >= self.max_turns:
            self.__finish()
