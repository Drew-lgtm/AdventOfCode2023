#!/usr/bin/env python

import sys

sys.setrecursionlimit(10**6)

# Using these values, 3-dir switches direction 180°
NORTH = 0
WEST = 1
EAST = 2
SOUTH = 3


class Tile:
    def __init__(
        self, x: int, y: int, type: str, is_start: bool = False, is_end: bool = False
    ):
        self.x = x
        self.y = y
        self.type = type
        self.inbound = [None] * 4
        self.outbound = [None] * 4
        self.visited = False
        self.is_start = is_start
        self.is_end = is_end

    def direction_allowed(self, dir) -> bool:
        """Returns True iff moving across this tile in direction dir is allowed"""
        return self.type == "." or self.type == "^><v"[dir]

    def connect(self, dir, other, ignore_dir=False):
        """Connects this tile to other for moving in direction dir. Ie, only connect outbound for this tile and inbound
        for other. Previously connected tiles in this direction will be overwritten.
        If either self or other is directional, only connects if the direction is allowed, unless ignore_dir is True.
        """
        if ignore_dir or (self.direction_allowed(dir) and other.direction_allowed(dir)):
            self.outbound[dir] = other
            other.inbound[3 - dir] = self

    def find_path(self) -> int:
        """Recursively finds the longest path to the end tile via DFS and returns the length of the path."""
        if self.is_end:
            return 1
        else:
            self.visited = True
            path_len = 0
            for next in self.outbound:
                if next and not next.visited:
                    path_len = max(path_len, next.find_path())
            self.visited = False
            # Only add the current tile to the path if we actually found a path to the end
            return (path_len > 0) + path_len

    def trace_path(self) -> int:
        """Recursively finds the longest path to the end tile via DFS and returns the tiles comprising the path."""
        if self.is_end:
            return {self}
        else:
            self.visited = True
            paths = []
            for next in self.outbound:
                if next and not next.visited:
                    paths.append(next.trace_path())
            self.visited = False
            if paths:
                longest_path = max(paths, key=len)
                if len(longest_path) > 0:
                    longest_path.add(self)
                return longest_path
            else:
                return set()


class BidirectionalTile:
    def __init__(self, x: int, y: int, is_start: bool = False, is_end: bool = False):
        self.x = x
        self.y = y
        self.adjacent = []
        self.visited = False
        self.is_start = is_start
        self.is_end = is_end

    def is_node(self) -> bool:
        """If a tile is connected to exactly 2 other tiles, it is part of a path and could be ignored. Otherwise it is
        either connected to 1 tile (endpoint) or more than 2 (junction).

        Returns True iff this tile is a node, ie a junction or an endpoint."""
        return len(self.adjacent) != 2

    def connect(self, other):
        """Connects this tile to other.

        NB: if other is already connected, they will be connected a second time!"""
        self.adjacent.append((1, other))
        other.adjacent.append((1, self))

    def join(self):
        """Assumes there are exactly 2 other tiles connected to this one. Joins those 2 directly, while retaiting the
        length of the path between them."""
        len_a, tile_a = self.adjacent[0]
        len_b, tile_b = self.adjacent[1]
        tile_a._replace((len_a, self), (len_a + len_b, tile_b))
        tile_b._replace((len_b, self), (len_a + len_b, tile_a))

    def _replace(self, other, new):
        """Looks for other among its adjacent tiles and replaces it with new.

        other: (int, BidirectionalTile), adjacent to self
        new: (int, BidirectionalTile), tuple of new distance and new tile"""
        idx = self.adjacent.index(other)
        self.adjacent[idx] = new

    def find_path(self) -> int:
        """Recursively finds the longest path to the end tile via DFS and returns the length of the path."""
        if self.is_end:
            return 1
        else:
            self.visited = True
            path_len = 0
            for dist, next in self.adjacent:
                if not next.visited:
                    d = next.find_path()
                    if d > 0:
                        path_len = max(path_len, dist + d)
            self.visited = False
            return path_len

    def trace_path(self):
        """Recursively finds the longest path to the end tile via DFS and returns the tiles comprising the path.
        Overcounts the length by 1."""
        if self.is_end:
            return (1, {self})
        else:
            current = (0, set())
            self.visited = True
            for dist, next in self.adjacent:
                if not next.visited:
                    d, next_path = next.trace_path()
                    if d > 0 and dist + d > current[0]:
                        next_path.add(self)
                        current = (dist + d, next_path)
            self.visited = False
            return current


with open("data.txt ", "r") as f:
    tiles = {}
    tiles2 = {}
    width = 0
    height = 0
    for y, line in enumerate(f.readlines()):
        height += 1
        for x, tile in enumerate(line.strip()):
            if y == 0:
                width += 1
            if tile != "#":
                # Assume only start on the first line
                last_tile = Tile(x, y, tile, is_start=(y == 0))
                last_tile2 = BidirectionalTile(x, y, is_start=(y == 0))
                tiles[(x, y)] = last_tile
                tiles2[(x, y)] = last_tile2
                above = (x, y - 1)
                before = (x - 1, y)
                if above in tiles:
                    last_tile.connect(NORTH, tiles[above])
                    tiles[above].connect(SOUTH, last_tile)
                    last_tile2.connect(tiles2[above])
                if before in tiles:
                    last_tile.connect(EAST, tiles[before])
                    tiles[before].connect(WEST, last_tile)
                    last_tile2.connect(tiles2[before])
    last_tile.is_end = True
    last_tile2.is_end = True

first_tile = (tile for tile in tiles.values() if tile.is_start).__next__()
first_tile2 = (tile for tile in tiles2.values() if tile.is_start).__next__()

for tile in tiles2.values():
    if not tile.is_node():
        tile.join()


# dist, path = first_tile2.trace_path()
# print("  ", end="")
# for x in range(width):
#     print(f"{x%10}", end="")
# print()
# for y in range(height):
#     print(f"{y%10} ", end="")
#     for x in range(width):
#         pos = (x, y)
#         if pos in tiles2:
#             cur = tiles2[pos]
#             if cur in path:
#                 if cur.is_start:
#                     print("s", end="")
#                 elif cur.is_end:
#                     print("e", end="")
#                 else:
#                     print("O", end="")
#             else:
#                 if cur.is_start:
#                     print("S", end="")
#                 elif cur.is_end:
#                     print("E", end="")
#                 elif cur.is_node():
#                     print("X", end="")
#                 else:
#                     print(".", end="")
#         else:
#             print("#", end="")
#     print()

# print(f"Dist: {dist}\n")

# -1 to compensate double counting the starting point
print(f"Part 1: {first_tile.find_path()-1}")
print(f"Part 2: {first_tile2.find_path()-1}")