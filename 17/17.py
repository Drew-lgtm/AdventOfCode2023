import numpy as np
from tqdm import trange
import heapq
DEFAULT_FILENAME = "data.txt"
def read_chars(filename = DEFAULT_FILENAME):
    res = []
    with open(filename, "r") as f:
        for li in f:
            res.append(np.array([int(e) for e in [*li.strip()]]))
    res = np.array(res)
    return res
Right = (0, 1)
Down = (1, 0)
Left = (0, -1)
Up = (-1, 0)

def dis_pathfind(world_map, min_conse, max_conse):
  visited = set()
  worklist = [(0, 0, 0, Right, 1), (0, 0, 0, Down, 1)] # cost, x, y, _dir, _dir_count
  l_c = -1
  while len(worklist) > 0:
    cost, x, y, _dir, _dir_count = heapq.heappop(worklist)
    if (x, y, _dir, _dir_count) in visited:
      continue
    else:
      visited.add((x, y, _dir, _dir_count))
    new_x = x + _dir[1]
    new_y = y + _dir[0]
    if new_x < 0 or new_y < 0 or new_x >= world_map.shape[1] or new_y >= world_map.shape[0]:
      continue
    new_cost = cost + world_map[new_y, new_x]
    if _dir_count >= min_conse and _dir_count <= max_conse:
      if new_x == world_map.shape[1] - 1 and new_y == world_map.shape[0] - 1:
        return new_cost
    for d in [Right, Down, Left, Up]:
      # no reverse
      if d[0] + _dir[0] == 0 and d[1] + _dir[1] == 0:
        continue
      new_d_count = _dir_count + 1 if d == _dir else 1
      if (d != _dir and _dir_count < min_conse) or new_d_count > max_conse:
        continue
      heapq.heappush(worklist, (new_cost, new_x, new_y, d, new_d_count))

print(f"Part 1: {dis_pathfind(read_chars(), 1, 3)}")
print(f"Part 2: {dis_pathfind(read_chars(), 4, 10)}")