import math
import os, sys
import time

class SeedMap:
    def __init__(self, off: str, to: str):
        self.off = off
        self.to = to
        # mapping values
        self.map_values: list[tuple[int, int, int]] = []
    def add(self, target: int, source: int, offset: int):
        self.map_values.append((source, source + offset, target))
    def get_destination(self, given: int):
        # for each mapping range
        for source, max_source, target in self.map_values:
            # if given is in between range
            if source <= given < max_source:
                # map it
                return target + (given - source)
        # if no range was found,
        # return value unchanged
        return given
    def __str__(self) -> str:
        return f"{self.off} => {self.to}"
    def __repr__(self) -> str:
        return self.__str__()


def main():
    with open(os.path.join(sys.path[0],"data.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
    lines = text.split("\n")
    
    # parse first line to get all seeds
    seeds = [int(s) for s in lines[0].split(": ")[1].split(" ")]
    # create seed maps
    seed_maps: list[SeedMap] = []
    current_map = None
    # for each other line except 1st line
    for line in lines[1:]:
        # skip empty lines
        if line == "":
            continue
        # if new map declaration start
        if line.endswith("map:"):
            # get from and to strings (just for printing)
            off, to = line.split(" ")[0].split("-to-", 1)
            # create new map
            current_map = SeedMap(off, to)
            # and add it to the list
            seed_maps.append(current_map)
        else:
            # the * will unpack the list into 3 arguments
            current_map.add(*[int(s) for s in line.split(" ")])
    min_location = math.inf
    # for each seed
    for seed in seeds:
        # map it through all seed maps
        for seed_map in seed_maps:
            seed = seed_map.get_destination(seed)
        # and update the minimum location
        min_location = min(min_location, seed)
    print(min_location)
            

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f} seconds")