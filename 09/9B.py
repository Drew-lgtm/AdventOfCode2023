with open('data.txt', 'r', encoding='utf-8') as f:
    table = [[int(x) for x in line.split()] for line in f.read().splitlines()]

f = lambda r: 0 if set(r)=={0} else r[-1] + f([b - a for a, b in zip(r, r[1:])])

print(f"Part 1: {sum(f(row) for row in table)}")
print(f"Part 2: {sum(f(row[::-1]) for row in table)}")