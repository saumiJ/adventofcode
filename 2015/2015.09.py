# Link to task: https://adventofcode.com/2022/day/9

import numpy as np
import re

from collections import defaultdict
from copy import deepcopy
from operator import gt, lt
from typing import List, Callable


with open("input/2015.09.in", "r") as f:
    lines = f.read().splitlines()

# read distances
places = list()
place_to_place_to_dist = defaultdict(dict)
for line in lines:
    res = re.search(r'([A-Z|a-z]+) to ([A-Z|a-z]+) = ([0-9]+)', line).groups()
    place_1, place_2, dist = res[0], res[1], int(res[2])
    place_to_place_to_dist[place_1][place_2] = dist
    place_to_place_to_dist[place_2][place_1] = dist
    for place in [place_1, place_2]:
        if place not in places:
            places.append(place)
num_places = len(places)

# populate distance-matrix
distmat = np.zeros(shape=(num_places, num_places), dtype=int)
for i, place_1 in enumerate(places):
    for j, place_2 in enumerate(places):
        if i == j:
            continue
        distmat[i, j] = place_to_place_to_dist[place_1][place_2]
        distmat[j, i] = place_to_place_to_dist[place_2][place_1]

min_dist = int(np.sum(distmat)) + 1
return_to_start = False
place_ids_set = set(range(num_places))


# curry the distance-function
def curry_calculate(res_func: Callable, comp_op: Callable, init_val):
    def calculate(cur: int, visited: List[int]) -> int:
        # mark current place as visited
        visited.append(cur)
        # find remaining places to visit
        todos = place_ids_set - set(visited)
        if len(todos) == 2:
            # only two places left to visit; return the optimal of the two, plus distance between the two
            place_a, place_b = todos
            ab_dist = distmat[place_a, place_b]
            return res_func(distmat[cur, place_a] + ab_dist, distmat[cur, place_b] + ab_dist)
        required_dist_to_cur = init_val
        for todo in todos:
            new_dist = calculate(todo, deepcopy(visited))
            compared_dist = distmat[cur, todo] + new_dist
            if comp_op(compared_dist, required_dist_to_cur):
                required_dist_to_cur = compared_dist
        return required_dist_to_cur
    return calculate


calc_min = curry_calculate(min, lt, np.inf)
calc_max = curry_calculate(max, gt, 0)

min_distance = min(calc_min(place_id, list()) for place_id in place_ids_set)
max_distance = max(calc_max(place_id, list()) for place_id in place_ids_set)
print(f"Trip distance (min | max): ({min_distance} | {max_distance})")
