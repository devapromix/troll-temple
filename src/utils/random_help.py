from random import randint
from typing import NamedTuple, List


class ChoiceBox(NamedTuple):
    obj: object
    weight: int


'''Analog of random.choice(), but use additional parameter ('weight'), which customize chance of random'''


def weighted_choice(boxes: List[ChoiceBox]) -> object:
    all_weight = sum([box.weight for box in boxes])
    number = randint(0, all_weight - 1)
    for (obj, weight) in boxes:
        if number < weight:
            return obj
        number -= weight
    assert False
