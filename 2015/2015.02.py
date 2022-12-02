# Link to task: https://adventofcode.com/2022/day/2

with open("input/2015.02.in", "r") as f:
    lines = f.readlines()

wrapping_paper_area = 0
ribbon_length = 0
for line in lines:
    line = line.strip("\n")
    l, w, h = (int(num_str) for num_str in line.split("x"))
    a1, a2, a3 = l * w, w * h, h * l
    p1, p2, p3 = 2 * (l + w), 2 * (w + h), 2 * (l + h)
    volume = l * w * h
    wrapping_paper_area += 2 * (a1 + a2 + a3) + min(a1, a2, a3)
    ribbon_length += min(p1, p2, p3) + volume
print(f"Total area of wrapping paper needed: {wrapping_paper_area} sq.ft.")
print(f"Total length of ribbon needed: {ribbon_length} ft.")
