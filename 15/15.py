from typing import List, Dict, Tuple

with open('data.txt') as file:
    sequence: List[str] = file.read().split(',')


def _hash(_s: str):
    h: int = 0
    for i in _s:
        h = (h + ord(i)) * 17 % 256
    return h


# Part 1
print(f'Part 1: {sum(_hash(i) for i in sequence)}')


# Part 2
boxes: Dict[int, Dict[str, int]] = {i: {} for i in range(256)}

for op in sequence:
    if op[-2] == '=':
        s, v = op.split('=')
        boxes[_hash(s)][s] = int(v)
    elif op[-1] == '-':
        s: str = op[:-1]
        hsh: int = _hash(s)
        if s in boxes[hsh]:
            del boxes[hsh][s]

print(f'Part 2: '
      f'{sum(sum((m + 1) * v * (i + 1) for i, v in enumerate(box.values())) for m, box in enumerate(boxes.values()))}')
