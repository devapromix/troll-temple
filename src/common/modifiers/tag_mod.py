from enum import Enum

from .modifier import Modifier


class Tag(Enum):
    BlockedAlwaysReflect = 'blocked_always_relfect'


class TagMod(Modifier):
    """
    Modifier, which add tag for mob.
    Tag - is a custom boolean attribute, which is contained in dict. For example, 'can_wear_weapon', 'blocked_always_relfect'
    """

    TAG_DESCRIPTIONS = {
        Tag.BlockedAlwaysReflect: "blocked damages always reflect",
    }
    """
    This dict contain a human-readable description of tag
    """

    def __init__(self, tag: Tag):
        self.tag = tag

    @property
    def descr(self):
        return self.TAG_DESCRIPTIONS[self.tag]

    def commit(self, mob):
        super().commit(mob)
        mob.tags[self.tag] = mob.tags.get(self.tag, 0) + 1

    def rollback(self, mob):
        super().rollback(mob)
        mob.tags[self.tag] = mob.tags.get(self.tag, 0) - 1
        if not mob.tags[self.tag] > 0:
            del mob.tags[self.tag]

    def try_union(self, other):
        return super().try_union(other) and self.tag == other.tag

