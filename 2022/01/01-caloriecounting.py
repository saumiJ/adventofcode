# read file
with open("01.in", "r") as f:
    lines = f.readlines()

# add a newline character to end of line-list
lines.append("\n")


# function to check if inventory of current elf is completed
def is_end_of_current_inventory(current_line: str) -> bool:
    return current_line == "\n"


# count calories
elf_with_max_calorie_count = -1
max_calorie_count = -1
current_elf = 0
current_elf_calorie_count = 0
for line in lines:
    if is_end_of_current_inventory(line):
        current_elf += 1
        if current_elf_calorie_count > max_calorie_count:
            elf_with_max_calorie_count = current_elf
            max_calorie_count = current_elf_calorie_count
        current_elf_calorie_count = 0
    else:
        current_elf_calorie_count += int(line)
total_elves = current_elf

print(f"Calorie-count of elf with most calories: {max_calorie_count}\n"
      f"Elf with most calories: {elf_with_max_calorie_count} out of {total_elves}\n"
      f"Note: Elf-IDs begin from 1")
