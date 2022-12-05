# link to task: https://adventofcode.com/2015/day/12

import json
import re


with open("input/2015.12.in", "r") as f:
    line = f.readline()

numbers = [int(n) for n in re.findall(r'(-?[0-9]+)', line)]
print(f"Answer to part-1: {sum(numbers)}")


forbidden_values = {"red"}


def traverse_list_and_sum_numbers(list_obj: list) -> int:
    return handle(list_obj)


def traverse_dict_and_sum_numbers(dict_obj: dict) -> int:
    dict_vals = dict_obj.values()
    for forbidden_value in forbidden_values:
        if forbidden_value in dict_vals:
            return 0
    return handle(dict_vals)


def handle(items: iter) -> int:
    my_sum = 0
    for item in items:
        if isinstance(item, list):
            my_sum += traverse_list_and_sum_numbers(item)
        elif isinstance(item, dict):
            my_sum += traverse_dict_and_sum_numbers(item)
        elif isinstance(item, str):
            try:
                my_sum += int(item)
            except ValueError:
                pass
        elif isinstance(item, int):
            my_sum += item
        else:
            raise NotImplementedError(item)
    return my_sum


config = json.loads(line)
print(f"Answer to part-1: {traverse_list_and_sum_numbers(config)}")
