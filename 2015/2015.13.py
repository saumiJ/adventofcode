# link to task: https://adventofcode.com/2015/day/12

import numpy as np
import re

from collections import defaultdict
from copy import deepcopy
from typing import List


with open("input/2015.13.in", "r") as f:
    lines = f.read().splitlines()

# read relations
people = list()
p1_to_p2_to_happiness = defaultdict(dict)
for line in lines:
    res = re.search(r'([A-Z|a-z]+) would ([a-z]+) ([0-9]+) happiness units by sitting next to ([A-Z|a-z]+)',
                    line).groups()
    person_1, gain_or_lose, happiness, person_2 = res[0], res[1], int(res[2]), res[3]
    sign = 1. if gain_or_lose == "gain" else -1
    p1_to_p2_to_happiness[person_1][person_2] = sign * happiness
    for person in [person_1, person_2]:
        if person not in people:
            people.append(person)
num_persons = len(people)

# populate happiness-matrix
hapmat = np.zeros(shape=(num_persons, num_persons), dtype=int)
hapmat_with_me = np.zeros(shape=(num_persons+1, num_persons+1), dtype=int)
for i, person_1 in enumerate(people):
    for j, person_2 in enumerate(people):
        if i == j:
            continue
        hapmat[i, j] = p1_to_p2_to_happiness[person_1][person_2] + p1_to_p2_to_happiness[person_2][person_1]
        hapmat[j, i] = hapmat[j, i]
        hapmat_with_me[i, j] = hapmat[i, j]
        hapmat_with_me[j, i] = hapmat[j, i]

person_ids_set = set(range(num_persons))
persons_ids_set_with_me = set(range(num_persons+1))


# happiness-function
def calculate(cur: int, visited: List[int], pids_set: set, _hapmat) -> int:
    # mark current person as seated
    visited.append(cur)
    # find remaining persons to seat
    todos = pids_set - set(visited)
    if len(todos) == 2:
        # only two persons left to seat
        person_a, person_b = todos
        cur_a_hap, cur_b_hap = _hapmat[cur, person_a], _hapmat[cur, person_b]  # their happiness with current
        ab_hap = _hapmat[person_a, person_b]  # their mutual happiness
        a0_hap, b0_hap = _hapmat[visited[0], person_a], _hapmat[visited[0], person_b]  # their happiness with first
        return max(cur_a_hap + ab_hap + b0_hap, cur_b_hap + ab_hap + a0_hap)
    required_happiness_to_cur = 0
    for todo in todos:
        new_happiness = calculate(todo, deepcopy(visited), pids_set, _hapmat)
        compared_happiness = _hapmat[cur, todo] + new_happiness
        if compared_happiness > required_happiness_to_cur:
            required_happiness_to_cur = compared_happiness
    return required_happiness_to_cur


print(f"Max-happiness: {max(calculate(person_id, list(), person_ids_set, hapmat) for person_id in person_ids_set)}")
print(f"Max-happiness with me at the table: "
      f"{max(calculate(person_id, list(), persons_ids_set_with_me, hapmat_with_me) for person_id in person_ids_set)}")
