import math

test_input = """
Time:      7  15   30
Distance:  9  40  200
"""

with open("data.txt") as f:
    input = f.read()
# print(input)

def parse_input(input: str):
    [times, distances] = input.strip().splitlines()
    times = [int(t) for t in times.removeprefix("Time: ").strip().split()]
    distances = [int(d) for d in distances.removeprefix("Distance: ").strip().split()]
    return list(zip(times, distances))

test_races = parse_input(test_input)
races = parse_input(input)

print(test_races)

def ways_to_win_a_race(race):
    (max_time, record_distance) = race
    ways = 0
    for hold_for in range(max_time + 1):
        distance = (max_time - hold_for) * hold_for
        if distance > record_distance:
            ways += 1
    return ways

# print(ways_to_win_a_race(test_races[2]))

def p1(races):
    return math.prod([ways_to_win_a_race(race) for race in races])

# print(p1(test_races))
print(p1(races))
# print(ways_to_win_a_race((71530, 940200)))
print(ways_to_win_a_race((48989083, 390110311121360)))
