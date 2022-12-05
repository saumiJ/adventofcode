# link to task: https://adventofcode.com/2022/day/5

import re

from copy import deepcopy


with open("input/2022.05.in", "r") as f:
    lines = f.read().splitlines()

# read crate-arrangement and movement-instructions
crate_stacks_input = list()
instructions = list()
for line in lines:
    if not line.startswith("move"):
        if line == "":
            continue
        crate_stacks_input.append(line)
    else:
        res = re.search(r'move ([0-9]+) from ([0-9]+) to ([0-9]+)', line)
        instructions.append([int(n) for n in res.groups()])

# parse crate-arrangement
stacks = [int(s) for s in re.findall(r'([0-9]+)', crate_stacks_input[-1])]
stack_to_crates = {s: [] for s in stacks}
for line in crate_stacks_input[-2::-1]:
    res = re.findall(r'(\[[A-Z]]| {4})', line)
    for i, crate in enumerate(res):
        if crate.startswith(" "):
            continue
        crate = crate.strip('[').strip(']')
        stack = stacks[i]
        stack_to_crates[stack].append(crate)


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
