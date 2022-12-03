# Link to task: https://adventofcode.com/2022/day/3

from string import ascii_lowercase, ascii_uppercase

with open("input/2022.03.in", "r") as f:
    lines = f.read().splitlines()

priority_list = [alp for alp in ascii_lowercase] + [alp for alp in ascii_uppercase]

priority_sum = 0
for line in lines:
    num_items = len(line)
    assert num_items % 2 == 0
    compartment_1_limit = int(num_items/2)
    items_compartment_1 = line[:compartment_1_limit]
    items_compartment_2 = line[compartment_1_limit:]
    common_items = set(items_compartment_1).intersection(set(items_compartment_2))
    assert len(common_items) == 1
    common_item = common_items.pop()
    priority_sum += priority_list.index(common_item) + 1
print(f"Priority-sum for part-1: {priority_sum}")

elf_group_size = 3
priority_sum = 0
for i, _ in enumerate(lines[::elf_group_size]):
    idx_1 = elf_group_size * i
    rs1 = lines[idx_1]
    rs2 = lines[idx_1 + 1]
    rs3 = lines[idx_1 + 2]
    common_items = set(rs1).intersection(set(rs2)).intersection(set(rs3))
    assert len(common_items) == 1, common_items
    common_item = common_items.pop()
    priority_sum += priority_list.index(common_item) + 1
print(f"Priority-sum for part-2: {priority_sum}")
