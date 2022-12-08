# link to task: https://adventofcode.com/2022/day/8

import numpy as np


with open("input/2022.08.in", "r") as f:
    lines = f.read().splitlines()

# assumption: all rows have the same length
len_x = len(lines[0])
len_y = len(lines)

heights = np.asarray([[int(h) for h in row] for row in lines])
is_visible = np.zeros(shape=(len_x, len_y), dtype=int)
scenic_score = np.ones_like(is_visible)

# borders are visible
is_visible[:, 0] = is_visible[:, -1] = is_visible[0, :] = is_visible[-1, :] = 1


def check_visibility(_tree_height: int, _cur_max: int) -> (int, int):
    if _tree_height > _cur_max:
        return 1, _tree_height
    else:
        return 0, _cur_max


def check_scenery(_readings: list, _tree_height: int) -> int:
    _score = 0
    for _r in _readings[::-1]:
        _score += 1
        if _r >= tree_height:
            break
    return _score


# TODO: refactor to remove code-duplication
# check rows
for i, row in enumerate(heights):
    cur_max = row[0]
    readings = []
    for j, tree_height in enumerate(row):
        scenic_score[i, j] *= check_scenery(readings, tree_height)
        incr, cur_max = check_visibility(tree_height, cur_max)
        is_visible[i, j] += incr
        readings.append(tree_height)

for i, row in enumerate(heights):
    cur_max = row[-1]
    readings = []
    for j, tree_height in enumerate(row[::-1]):
        j_ind = len_y - j - 1
        scenic_score[i, j_ind] *= check_scenery(readings, tree_height)
        incr, cur_max = check_visibility(tree_height, cur_max)
        is_visible[i, j_ind] += incr
        readings.append(tree_height)

# check columns
for j, col in enumerate(heights.transpose()):
    cur_max = col[0]
    readings = []
    for i, tree_height in enumerate(col):
        scenic_score[i, j] *= check_scenery(readings, tree_height)
        incr, cur_max = check_visibility(tree_height, cur_max)
        is_visible[i, j] += incr
        readings.append(tree_height)

for j, col in enumerate(heights.transpose()):
    cur_max = col[-1]
    readings = []
    for i, tree_height in enumerate(col[::-1]):
        i_ind = len_x - i - 1
        scenic_score[i_ind, j] *= check_scenery(readings, tree_height)
        incr, cur_max = check_visibility(tree_height, cur_max)
        is_visible[i_ind, j] += incr
        readings.append(tree_height)

print(f"Number of visible trees: {len(is_visible[np.where(is_visible > 0)])}")
print(f"Max scenic score: {np.max(scenic_score)}")
