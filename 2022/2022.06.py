# link to task: https://adventofcode.com/2022/day/6

with open("input/2022.06.in", "r") as f:
    signal = f.readline()


def find_marker_position(sgnl: str, sequence_size: int) -> int:
    last_n = list()
    for i, c in enumerate(sgnl):
        last_n.append(c)
        len_last_n = len(last_n)
        if len_last_n < sequence_size:
            continue
        elif len_last_n > sequence_size:
            last_n.pop(0)
        if len(last_n) == len(set(last_n)):
            return i + 1
    raise ValueError("start of packet marker not found!")


print(f"Start-of-packet marker position: {find_marker_position(signal, sequence_size=4)}")
print(f"Start-of-message marker position: {find_marker_position(signal, sequence_size=14)}")
