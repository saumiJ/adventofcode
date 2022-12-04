# Link to task: https://adventofcode.com/2022/day/5

with open("input/2015.05.in", "r") as f:
    lines = f.read().splitlines()

vowels = ["a", "e", "i", "o", "u"]
forbidden_strings = ["ab", "cd", "pq", "xy"]


def is_nice_part_1(string: str) -> bool:
    len_string = len(string)

    num_vowels = 0
    contains_twins = False
    for i, char in enumerate(string):
        num_vowels += 1 if char in vowels else 0
        if i < len_string - 1 and char == string[i + 1]:
            contains_twins = True

    contains_forbidden_strings = False
    for forbidden_string in forbidden_strings:
        if forbidden_string in string:
            contains_forbidden_strings = True
            break

    return num_vowels >= 3 and contains_twins and not contains_forbidden_strings


def is_nice_part_2(string: str) -> bool:
    len_string = len(string)

    fulfils_rule_1 = False
    fulfils_rule_2 = False

    for i, char in enumerate(string):
        if i == len_string - 1:
            continue
        pair = f"{char}{string[i + 1]}"
        string_without_this_pair = string.replace(pair, "")
        if len_string - len(string_without_this_pair) > 3:
            fulfils_rule_1 = True
            break

    for i, char in enumerate(string):
        if i < len_string - 2 and char == string[i+2]:
            fulfils_rule_2 = True
            break

    return fulfils_rule_1 and fulfils_rule_2


num_nice_strings_part_1 = 0
num_nice_strings_part_2 = 0
for _string in lines:
    _string = _string.lower()
    num_nice_strings_part_1 += int(is_nice_part_1(_string))
    num_nice_strings_part_2 += int(is_nice_part_2(_string))
print(f"Number of nice strings (part-1): {num_nice_strings_part_1}")
print(f"Number of nice strings (part-2): {num_nice_strings_part_2}")
