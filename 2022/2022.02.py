# Link to task: https://adventofcode.com/2022/day/2

import functools

from enum import Enum


class Shape(Enum):
    Rock = "A"
    Paper = "B"
    Scissors = "C"

    def __init__(self, label):
        self.label = label
        self.id, self.score = (0, 1) if label == "A" else ((1, 2) if label == "B" else (2, 3))

    def beats(self) -> "Shape":
        return {
            Shape.Rock: Shape.Scissors,
            Shape.Paper: Shape.Rock,
            Shape.Scissors: Shape.Paper
        }[self]

    def draws(self) -> "Shape":
        return self

    def loses_to(self) -> "Shape":
        return {
            Shape.Rock: Shape.Paper,
            Shape.Paper: Shape.Scissors,
            Shape.Scissors: Shape.Rock
        }[self]


class Strategy(Enum):
    SHAPE = "SHAPE"
    OUTCOME = "OUTCOME"

    def get_shapes(self, input_str: str) -> (Shape, Shape):
        first, second = input_str.split(" ")
        op_shape = Shape(first)
        if self is Strategy.SHAPE:
            my_shape = {
                "X": Shape.Rock,
                "Y": Shape.Paper,
                "Z": Shape.Scissors,
            }[second]
        elif self is Strategy.OUTCOME:
            my_shape = {
                "X": op_shape.beats(),
                "Y": op_shape.draws(),
                "Z": op_shape.loses_to()
            }[second]
        else:
            raise NotImplementedError(self)
        return op_shape, my_shape


@functools.lru_cache(maxsize=None)
def round_score(shapes: (Shape, Shape)) -> int:
    op, me = shapes
    outcome_score_matrix = [
        [3, 6, 0],
        [0, 3, 6],
        [6, 0, 3],
    ]
    score = outcome_score_matrix[op.id][me.id] + me.score
    return score


# read strategy guide
with open("input/2022.02.in", "r") as f:
    lines = f.read().splitlines()

part_1_strategy = Strategy.SHAPE
part_2_strategy = Strategy.OUTCOME
total_score_part_1 = 0
total_score_part_2 = 0
for line in lines:
    total_score_part_1 += round_score(part_1_strategy.get_shapes(line))
    total_score_part_2 += round_score(part_2_strategy.get_shapes(line))
print(f"Part-1 score: {total_score_part_1}\n"
      f"Part-2 score: {total_score_part_2}\n")
