from common.game_class import Game

from common.modifiers.tag_mod import *
from mobs.player import Player, Classes


class TestTagMod:
    mob = Player(0, Classes.FIGHTER)
    tag = Tag.BlockedAlwaysReflect
    tagMod = TagMod(Tag.BlockedAlwaysReflect)

    def test_single_tag(self):
        assert self.tag not in self.mob.tags.keys()
        self.tagMod.commit(self.mob)
        assert self.tag in self.mob.tags.keys()
        self.tagMod.rollback(self.mob)
        assert self.tag not in self.mob.tags.keys()

    def test_multiple_committed_tag(self):
        assert self.tag not in self.mob.tags.keys()
        self.tagMod.commit(self.mob)
        self.tagMod.commit(self.mob)
        assert self.tag in self.mob.tags.keys()
        assert self.mob.tags[self.tag] == 2
        self.tagMod.rollback(self.mob)
        assert self.tag in self.mob.tags.keys()
        self.tagMod.rollback(self.mob)
        assert self.tag not in self.mob.tags.keys()

