# Link to task: https://adventofcode.com/2022/day/1

import numpy as np


def is_end_of_current_inventory(current_line: str) -> bool:
    """check if inventory of current elf is completed"""
    return current_line == "\n"


# read file
with open("input/2022.01.in", "r") as f:
    lines = f.readlines()

# add a newline character to end of line-list
lines.append("\n")


# count calories
elf_calorie_list = list()
elf_with_max_calorie_count = -1
current_elf_calorie_count = 0
for line in lines:
    if is_end_of_current_inventory(line):
        elf_calorie_list.append(current_elf_calorie_count)
        current_elf_calorie_count = 0
    else:
        current_elf_calorie_count += int(line)
total_elves = len(elf_calorie_list)

# part-1: find elf with maximum calorie-count (and the number of calories [s]he has)
sorted_calorie_count = np.sort(elf_calorie_list)[::-1]  # reversed
elves_sorted_by_calorie_count = np.argsort(elf_calorie_list)[::-1] + 1  # reversed, start indexing from 1
max_calorie_count = sorted_calorie_count[0]
elf_with_max_calorie_count = elves_sorted_by_calorie_count[0]
print(f"Calorie-count of elf with most calories: {max_calorie_count}\n"
      f"Elf with most calories: {elf_with_max_calorie_count} out of {total_elves}\n"
      f"Note: Elf-IDs begin from 1\n")

# part-2: find the top three elves carrying the most calories (and the total calories carried by them)
top_n = 3
top_n_elves = elves_sorted_by_calorie_count[:top_n]
top_n_calorie_count_total = np.sum(sorted_calorie_count[:top_n])
print(f"Top {top_n} calories total: {top_n_calorie_count_total}\n"
      f"Elves with top {top_n} calorie-count: {top_n_elves}\n"
      f"Note: Elf-IDs begin from 1\n")
