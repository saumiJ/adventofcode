# link to task: https://adventofcode.com/2022/day/7

import re
from copy import deepcopy
from typing import List


def is_eof(_lid: int, _num_lines: int) -> bool:
    return _lid >= _num_lines


def increment_lid(_lid: int, _lines: List[str]) -> (int, str):
    try:
        return _lid + 1, _lines[_lid + 1]
    except IndexError:
        # end-of-file
        return _lid + 1, None


def get_line(_lines: list, _lid: int) -> str:
    return _lines[_lid]


def is_cmd(line: str) -> bool:
    return re.match(r'\$ (.*)', line) is not None


def is_cd(line: str) -> bool:
    return line.startswith("$ cd")


def get_cd_target(line: str) -> str:
    res = re.findall(r'\$ cd (.*)', line)
    assert len(res) == 1
    return res[0]


def is_ls(line: str) -> bool:
    return line.startswith("$ ls")


def is_directory(line: str) -> bool:
    return line.startswith("dir ")


def get_directory_name(line: str) -> str:
    res = re.findall(r'dir (.*)', line)
    assert len(res) == 1
    return res[0]


def set_directory_contents(_file_tree: dict, absolute_path: List[str], contents: dict):
    for directory in absolute_path[:-1]:
        _file_tree = _file_tree.setdefault(directory, {})
    _file_tree[absolute_path[-1]] = contents


def get_file_name_and_size(line: str) -> (str, int):
    res = re.findall(r'([0-9]+) (.*)', line)
    assert len(res) == 1
    file_size_str, _file_name = res[0]
    return _file_name, int(file_size_str)


def get_absolute_path(_cur_dir: List[str], _root: str) -> str:
    return _root + '/'.join(_cur_dir[1:])


with open("input/2022.07.in", "r") as f:
    lines = f.read().splitlines()

root = "/"
move_up = ".."
num_lines = len(lines)
file_tree = {root: dict()}
abs_path_to_size = dict()
cur_dir = [root]

# construct file-tree structure, simultaneously record sizes of all files in each directory
lid = 0
while not is_eof(lid, num_lines):
    cur_line = lines[lid]
    if is_cmd(cur_line):
        if is_cd(cur_line):
            cd_target = get_cd_target(cur_line)
            if cd_target == root:
                cur_dir = [root]
            elif cd_target == move_up:
                cur_dir.pop()
            else:
                cur_dir.append(cd_target)
            lid, cur_line = increment_lid(lid, lines)
        elif is_ls(cur_line):
            cur_dir_contents = dict()
            cur_dir_file_size_count = 0
            lid, cur_line = increment_lid(lid, lines)
            while not (is_eof(lid, num_lines) or is_cmd(cur_line)):
                if is_directory(cur_line):
                    directory_name = get_directory_name(cur_line)
                    cur_dir_contents[directory_name] = dict()
                else:
                    file_name, file_size = get_file_name_and_size(cur_line)
                    cur_dir_contents[file_name] = file_size
                    cur_dir_file_size_count += file_size
                lid, cur_line = increment_lid(lid, lines)
            set_directory_contents(file_tree, cur_dir, cur_dir_contents)
            abs_path_to_size[get_absolute_path(cur_dir, root)] = cur_dir_file_size_count
        else:
            raise NotImplementedError(cur_line)
    else:
        raise NotImplementedError(cur_line)

abs_path_to_total_size = deepcopy(abs_path_to_size)
for focus_path in abs_path_to_size:
    for compared_path, compared_path_size in abs_path_to_size.items():
        if focus_path != compared_path and focus_path in compared_path:
            abs_path_to_total_size[focus_path] += compared_path_size

count_size_limit = 100000
cumulative_sizes_of_all_directories_whose_total_sizes_leq_count_size_limit = \
    sum((s for s in abs_path_to_total_size.values() if s <= count_size_limit))
print(f"Answer to part-1: {cumulative_sizes_of_all_directories_whose_total_sizes_leq_count_size_limit}")

total_disk_space = 70000000
required_disk_space = 30000000
used_space = abs_path_to_total_size[root]
free_disk_space = total_disk_space - used_space
target_space_to_be_freed = required_disk_space - free_disk_space

candidate_sizes = [s for s in abs_path_to_total_size.values() if s >= target_space_to_be_freed]
size_of_directory_to_delete = min(candidate_sizes)
print(f"Answer to part-2: {size_of_directory_to_delete}")
