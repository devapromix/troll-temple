class EffectsContainer:
    def __init__(self, owner):
        self.array = []
        self.owner = owner

    def add(self, effect):
        if effect in self:
            return
        effect.register(self.owner, lambda x: self.__on_effect_finished(x))
        self.array.append(effect)
        print(effect)

    def __on_effect_finished(self, effect):
        self.array.remove(effect)

    def __contains__(self, item):
        for ef in self.array:
            if ef is item:
                return True
        return False

    def act(self):
        for effect in self.array:
            effect.act()
