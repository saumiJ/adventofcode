# link to task: https://adventofcode.com/2022/day/5

import re

from copy import deepcopy


with open("input/2022.05.in", "r") as f:
    lines = f.read().splitlines()

instructions = list()
for line in lines:
    if not line.startswith("move"):
        continue

    res = re.search(r'move ([0-9]+) from ([0-9]+) to ([0-9]+)', line)
    instructions.append([int(n) for n in res.groups()])

# TODO: automate reading crate-arrangement
stack_to_crates = {
    1: ["B", "P", "N", "Q", "H", "D", "R", "T"],
    2: ["W", "G", "B", "J", "T", "V"],
    3: ["N", "R", "H", "D", "S", "V", "M", "Q"],
    4: ["P", "Z", "N", "M", "C"],
    5: ["D", "Z", "B"],
    6: ["V", "C", "W", "Z"],
    7: ["G", "Z", "N", "C", "V", "Q", "L", "S"],
    8: ["L", "G", "J", "M", "D", "N", "V"],
    9: ["T", "P", "M", "F", "Z", "C", "G"]
}
stacks = range(1, len(stack_to_crates.keys())+1)


def top_crates_after_rearrangement(s2c: dict, one_at_a_time: bool) -> str:
    for (num_crates, from_stack, to_stack) in instructions:
        if one_at_a_time:
            for _ in range(num_crates):
                crate = s2c[from_stack].pop()
                s2c[to_stack].append(crate)
        else:
            s2c[to_stack].extend(s2c[from_stack][-num_crates:])
            del s2c[from_stack][-num_crates:]
    return "".join([s2c[s][-1] for s in stacks])


print(f"Top-crates after rearrangement with CrateMover 9000: "
      f"{top_crates_after_rearrangement(deepcopy(stack_to_crates), one_at_a_time=True)}\n"
      f"Top-crates after rearrangement with CrateMover 9001: "
      f"{top_crates_after_rearrangement(deepcopy(stack_to_crates), one_at_a_time=False)}")
