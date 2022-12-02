# Link to task: https://adventofcode.com/2022/day/3

from copy import deepcopy

Address = (int, int)

with open("input/2015.03.in", "r") as f:
    lines = f.readlines()


def move_to_new_address(current_address: Address, instr: str) -> Address:
    return (
        current_address[0] + (1 if instr == ">" else (-1 if instr == "<" else 0)),
        current_address[1] + (1 if instr == "^" else (-1 if instr == "v" else 0)),
    )


_current_address = (0, 0)
addresses_with_at_least_one_present = {_current_address}
for line in lines:
    for _instr in line:
        _current_address = move_to_new_address(_current_address, _instr)
        addresses_with_at_least_one_present.add(_current_address)
print(f"Number of addresses with at least one present: {len(addresses_with_at_least_one_present)}")


def human_santa_delivers(instr_id: int) -> bool:
    return instr_id % 2 == 0


human_santa_current_address = (0, 0)
robo_santa_current_address = deepcopy(human_santa_current_address)
addresses_with_at_least_one_present = {human_santa_current_address}
for line in lines:
    for i, _instr in enumerate(line):
        if human_santa_delivers(i):
            human_santa_current_address = move_to_new_address(human_santa_current_address, _instr)
            addresses_with_at_least_one_present.add(human_santa_current_address)
        else:
            robo_santa_current_address = move_to_new_address(robo_santa_current_address, _instr)
            addresses_with_at_least_one_present.add(robo_santa_current_address)
print(f"Next year's number of addresses with at least one present: {len(addresses_with_at_least_one_present)}")
