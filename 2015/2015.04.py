# Link to task: https://adventofcode.com/2022/day/4

import hashlib

with open("input/2015.04.in", "r") as f:
    secret_key = f.readline()

i = 1
found_part_1 = False
found_part_2 = False
while not (found_part_1 and found_part_2):
    hash_val = hashlib.md5(f"{secret_key}{i}".encode("utf-8")).hexdigest()
    if hash_val.startswith("00000") and not found_part_1:
        print(f"Required number for part-1: {i}, hash-value: {hash_val}")
        found_part_1 = True
    if hash_val.startswith("000000") and not found_part_2:
        print(f"Required number for part-2: {i}, hash-value: {hash_val}")
        found_part_2 = True
    i += 1
