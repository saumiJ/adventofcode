# Link to task: https://adventofcode.com/2022/day/6

import numpy as np
import matplotlib.pyplot as plt

from enum import Enum


Coords = (int, int)


def extract_coords(coords_str: str) -> Coords:
    x_str, y_str = coords_str.split(",")
    return int(x_str), int(y_str)


class Action(Enum):
    ON = "turnon"
    OFF = "turnoff"
    TOGGLE = "toggle"

    def apply_part_1(self, start: Coords, stop: Coords, grd: np.ndarray):
        (start_x, start_y), (stop_x, stop_y) = start, stop
        grd_slice = grd[start_x: stop_x+1, start_y: stop_y+1]
        if self is Action.ON:
            grd_slice = np.logical_or(grd_slice, True)
        elif self is Action.OFF:
            grd_slice = np.logical_and(grd_slice, False)
        elif self is Action.TOGGLE:
            grd_slice = np.logical_not(grd_slice)
        else:
            raise NotImplementedError
        grd[start_x: stop_x+1, start_y: stop_y+1] = grd_slice
        return grd

    def apply_part_2(self, start: Coords, stop: Coords, grd: np.ndarray):
        (start_x, start_y), (stop_x, stop_y) = start, stop
        grd_slice = grd[start_x: stop_x + 1, start_y: stop_y + 1]
        if self is Action.ON:
            grd_slice += 1
        elif self is Action.OFF:
            grd_slice -= 1
            grd_slice = np.maximum(grd_slice, 0)
        elif self is Action.TOGGLE:
            grd_slice += 2
        else:
            raise NotImplementedError
        grd[start_x: stop_x + 1, start_y: stop_y + 1] = grd_slice
        return grd


with open("input/2015.06.in", "r") as f:
    lines = f.read().splitlines()

num_lights_per_row = 1000
_grd_part_1 = np.zeros(shape=(num_lights_per_row, num_lights_per_row), dtype=bool)
_grd_part_2 = np.zeros(shape=(num_lights_per_row, num_lights_per_row), dtype=int)

for line in lines:
    line = line.replace("turn ", "turn")
    action_label, start_str, _, stop_str = line.split(" ")
    _grd_part_1 = Action(action_label).apply_part_1(extract_coords(start_str), extract_coords(stop_str), _grd_part_1)
    _grd_part_2 = Action(action_label).apply_part_2(extract_coords(start_str), extract_coords(stop_str), _grd_part_2)

print(f"Number of lights on (part-1): {np.count_nonzero(_grd_part_1)}")
print(f"Total brightness (part-2): {np.sum(_grd_part_2)}")

plt.imshow(_grd_part_2)
plt.show()
