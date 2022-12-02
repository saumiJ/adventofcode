# Link to task: https://adventofcode.com/2022/day/1

with open("input/2015.01.in", "r") as f:
    lines = f.readlines()

floor = 0
first_basement_instruction_position = -1
for line in lines:
    for i, instruction in enumerate(line):
        floor += (1 if instruction == "(" else (-1 if instruction == ")" else 0))
        if floor == -1 and first_basement_instruction_position == -1:
            first_basement_instruction_position = i + 1

print(f"Target floor for Santa: {floor}\n"
      f"Position of instruction that causes Santa to first enter the basement: {first_basement_instruction_position}")
