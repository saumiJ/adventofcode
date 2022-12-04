# Link to task: https://adventofcode.com/2015/day/10

with open("input/2015.10.in", "r") as f:
    number_input = f.readline()

n_cycles_list = [40, 50]
for n_cycles in n_cycles_list:
    number_in = number_input
    for i in range(n_cycles):
        cur = number_in[0]
        numbers = [cur]
        counts = [0]
        for c in number_in:
            if c == cur:
                counts[-1] += 1
            else:
                cur = c
                numbers.append(cur)
                counts.append(1)
        number_in = "".join([f"{c}{n}" for c, n in zip(counts, numbers)])
    print(f"Number of digits after {n_cycles} cycles: {len(number_in)}")
