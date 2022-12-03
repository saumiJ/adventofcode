# Link to task: https://adventofcode.com/2022/day/8

import re
import logging

logging.getLogger().setLevel(logging.ERROR)

with open("input/2015.08.in", "r") as f:
    lines = f.read().splitlines()

total_code_chars_for_string_literals = 0
total_chars_in_memory = 0
for line in lines:
    num_code_chars_for_string_literals = len(line)
    logging.debug(f"\n{line}\n"
                  f"{''.join(['-' for _ in range(num_code_chars_for_string_literals)])}")
    total_code_chars_for_string_literals += num_code_chars_for_string_literals
    num_chars_in_memory = num_code_chars_for_string_literals

    # test for start- and end-double-quotes
    if line.startswith('"') and line.endswith('"'):
        num_chars_in_memory -= 2
        logging.debug(f"2 border-dquotes")

    # test for escaped back-slashes
    slashes = re.findall(r"(\\\\)", line)
    num_slashes = len(slashes)
    num_chars_in_memory -= num_slashes
    for slash in slashes:
        line = line.replace(slash, "")
    logging.debug(f"{num_slashes} slashes")

    # test for escaped double-quotes
    dquotes = re.findall(r'(\\")', line)
    num_dquotes = len(dquotes)
    num_chars_in_memory -= num_dquotes
    for dquote in dquotes:
        line = line.replace(dquote, "")
    logging.debug(f"{num_dquotes} quotes")

    # test for hexadecimal-represented ASCII
    num_hex_ascii = len(re.findall(r'(\\x([0-9]|[a-f]){2})', line))
    num_chars_in_memory -= 3 * num_hex_ascii
    logging.debug(f"{num_hex_ascii} hex-asciis")

    total_chars_in_memory += num_chars_in_memory
    logging.debug(f"ncc: {num_code_chars_for_string_literals}, ncm: {num_chars_in_memory}")
print(f"\nResult (part-1): {total_code_chars_for_string_literals - total_chars_in_memory}")

total_code_chars_for_string_literals_after_encoding = 0
for line in lines:
    line = line.replace("\\", "\\\\")
    line = line.replace("\"", "\\\"")
    line = '"' + line + '"'
    total_code_chars_for_string_literals_after_encoding += len(line)
print(f"\nResult (part-2): "
      f"{total_code_chars_for_string_literals_after_encoding - total_code_chars_for_string_literals}")
