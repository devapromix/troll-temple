from random import randint
from typing import NamedTuple, List


class ChoiceBox(NamedTuple):
    obj: object
    weight: int


'''Analog of random.choice(), but use additional parameter ('weight'), which customize chance of random'''


def weighted_choice_int(weights: List[int]) -> int:
    all_weight = sum(weights)
    number = randint(0, all_weight - 1)
    for (i, weight) in enumerate(weights):
        if number < weight:
            return i
        number -= weight


def weighted_choice(boxes: List[ChoiceBox]) -> object:
    choice_index = weighted_choice_int([box.weight for box in boxes])
    return boxes[choice_index].obj


def weighted_sample(boxes: List[ChoiceBox], count: int):  # TODO: check for another versions -> List[object | type]:
    if len(boxes) > count:
        results = []
        for i in range(count):
            choice = boxes[weighted_choice_int([box.weight for box in boxes])]
            results.append(choice.obj)
            boxes.remove(choice)
        return results
    else:
        return [box.obj for box in boxes]
