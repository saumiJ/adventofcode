# Link to task: https://adventofcode.com/2022/day/2

import functools


rck = (0, "rock    ")
ppr = (1, "paper   ")
scr = (2, "scissors")


@functools.lru_cache(maxsize=None)
def shape_to_shape_id(shape: str) -> (int, str):
    """Convert shape-name to shape-index. Tool-indices: Rock = 0, Paper = 1, Scissors = 2"""
    return {
        "A": rck,
        "X": rck,
        "B": ppr,
        "Y": ppr,
        "C": scr,
        "Z": scr,
    }[shape]


@functools.lru_cache(maxsize=None)
def id_to_shape_score(shape_id: int) -> int:
    """Convert shape-id to shape-score"""
    return {
        0: 1,
        1: 2,
        2: 3
    }[shape_id]


@functools.lru_cache(maxsize=None)
def round_score(op: str, me: str) -> int:
    outcome_score_matrix = [
        [3, 6, 0],
        [0, 3, 6],
        [6, 0, 3],
    ]
    (op_id, op_n), (me_id, me_n) = shape_to_shape_id(op), shape_to_shape_id(me)
    score = outcome_score_matrix[op_id][me_id] + id_to_shape_score(me_id)
    return score


# read strategy guide
with open("02.in", "r") as f:
    lines = f.readlines()

# play with given strategy
total_score = 0
for line in lines:
    line = line.strip("\n")
    (_op, _me) = line.split(" ")
    total_score += round_score(_op, _me)
print(f"Total score following strategy-guide: {total_score}")
