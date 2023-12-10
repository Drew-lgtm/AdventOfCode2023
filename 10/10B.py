from pathlib import Path
from time import time

then = time()

file = Path(__file__).parent / "data.txt"
lines = file.read_text().split("\n")


# shoelace theorem
def shoelace(points):
    area = 0

    X = [point[0] for point in points] + [points[0][0]]
    Y = [point[1] for point in points] + [points[0][1]]

    for i in range(len(points)):
        area += X[i] * Y[i + 1] - Y[i] * X[i + 1]

    return abs(area) / 2


# up, down, right, left
steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# (from): (to)
pipes = {
    "|": {(1, 0): (1, 0), (-1, 0): (-1, 0)},
    "-": {(0, 1): (0, 1), (0, -1): (0, -1)},
    "L": {(1, 0): (0, 1), (0, -1): (-1, 0)},
    "J": {(0, 1): (-1, 0), (1, 0): (0, -1)},
    "F": {(-1, 0): (0, 1), (0, -1): (1, 0)},
    "7": {(0, 1): (1, 0), (-1, 0): (0, -1)},
}

bends = ["L", "J", "F", "7"]

# create the map
M = []
for r, line in enumerate(lines):
    row = []
    for c, char in enumerate(line):
        row.append(char)
        if char == "S":
            r0, c0 = r, c
    M.append(row)

for dr, dc in steps:
    r, c = r0 + dr, c0 + dc
    V = [(r0, c0)]  # track vertices
    b = 1  # count boundary points

    while M[r][c] != "S":
        if not -1 < r < len(M) and -1 < c < len(M[r]):
            break  # out of bounds

        if not M[r][c] in pipes:
            break  # not a pipe

        pipe = pipes[M[r][c]]
        if not (dr, dc) in pipe:
            break  # pipes don't join up

        b += 1
        if M[r][c] in bends:
            V.append((r, c))

        dr, dc = pipe[(dr, dc)]
        r, c = r + dr, c + dc

    if M[r][c] == "S":
        break

A = shoelace(V)  # area

# pick's theorem
print(A + 1 - b / 2)

print(time() - then, "s")