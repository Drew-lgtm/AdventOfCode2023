from pathlib import Path
from time import time

then = time()

file = Path(__file__).parent / "data.txt"
lines = file.read_text().split("\n")

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

# create the map
M = []
for r, line in enumerate(lines):
    row = []
    for c, char in enumerate(line):
        row.append(char)
        if char == "S":
            r0, c0 = r, c
    M.append(row)

A = 0
for dr, dc in steps:
    r, c = r0 + dr, c0 + dc
    l = 1  # the length of the path

    while M[r][c] != "S":
        if not -1 < r < len(M) and -1 < c < len(M[r]):
            break  # out of bounds

        if not M[r][c] in pipes:
            break  # not a pipe

        pipe = pipes[M[r][c]]
        if not (dr, dc) in pipe:
            break  # pipes don't join up

        l += 1
        dr, dc = pipe[(dr, dc)]
        r, c = r + dr, c + dc

    if M[r][c] == "S":
        A = l // 2
        break

print(A)
print(time() - then, "s")