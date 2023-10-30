from mobs.effects.effect import Effect


class UniEffect(Effect):
    def __init__(self, modifier, max_turns):
        super().__init__()
        self.modifier = modifier
        self.max_turns = max_turns
