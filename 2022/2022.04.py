import re


with open("input/2022.04.in", "r") as f:
    lines = f.read().splitlines()

num_enclosures = 0
num_overlaps = 0
for line in lines:
    srch = re.search(r'([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)', line)
    s1, f1, s2, f2 = (int(n) for n in srch.groups())
    if s1 <= s2 <= f1 or s1 <= f2 < f1 or s2 <= s1 < f2 or s2 <= f1 <= f2:
        num_overlaps += 1
        if s1 <= s2 <= f2 <= f1 or s2 <= s1 <= f1 <= f2:
            num_enclosures += 1
print(f"Number of enclosing pairs: {num_enclosures}\n"
      f"Number of overlapping pairs: {num_overlaps}")
