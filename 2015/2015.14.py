import re


with open("input/2015.14.in", "r") as f:
    lines = f.read().splitlines()

total_time = 2503 # seconds

def compute_distance(speed: int, fly_time: int, rest_time: int, time_elapsed: int) -> int:
    cycle_time = fly_time + rest_time
    num_cycles = time_elapsed // cycle_time
    remaining_time = time_elapsed % cycle_time
    distance = num_cycles * speed * fly_time
    if remaining_time > fly_time:
        distance += speed * fly_time
    else:
        distance += speed * remaining_time
    return distance

reindeer_name_to_properties = {}
SPEED = 0
FLY_TIME = 1
REST_TIME = 2

winning_distance = 0

for line in lines:
    res = re.search(r'([A-Z|a-z]+) can fly ([0-9]+) km/s for ([0-9]+) seconds, but then must rest for ([0-9]+) seconds.',
                    line).groups()
    reindeer_name, speed, fly_time, rest_time = res[0], int(res[1]), int(res[2]), int(res[3])
    reindeer_name_to_properties[reindeer_name] = (speed, fly_time, rest_time)

for reindeer_name, properties in reindeer_name_to_properties.items():
    speed, fly_time, rest_time = properties
    winning_distance = max(winning_distance, compute_distance(speed, fly_time, rest_time, total_time))

print(f"Winning distance: {winning_distance}")
