#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict
from dataclasses import dataclass
from itertools import chain


@dataclass
class Mapping:
    dest: int
    source: int
    range_len: int

    def inside(self, input):
        return input in range(self.source, self.source + self.range_len)

    def apply(self, input):
        return input - self.source + self.dest

    def start(self):
        return self.source

    def end(self): # inclusive
        return self.source + self.range_len - 1

    def offset(self):
        return self.dest - self.source

    def to_range_map(self) -> "RangeMap":
        return RangeMap(self.start(), self.end(), self.offset())


@dataclass(frozen=True)
class RangeMap:
    start: int
    end: int # inclusive
    offset: int # apply to any number to get new value

    def __post_init__(self):
        assert self.end + self.offset >= 0, f"Invalid Rangemap! {self}"



    def apply(self, r) -> List["RangeMap"]:
        """
        A RangeMap applying another will result in 1 or more RangeMap.
        The part r not covered by the self rangeMap is not returned
        """
        print("Apply:", self, r)
        # no overlap, no changes
        if r.end < self.start or r.start > self.end:
            return [self]

        # "r" covers the start but not the end of self
        if r.start <= self.start and r.end < self.end:
            # Return modified first part and keept offset for the rest
            return [RangeMap(self.start, r.end, self.offset + r.offset), # self + r
                    RangeMap(r.end + 1, self.end, self.offset) # Unmodified
                    ]

        # "r" covers the end but not the start
        if r.start > self.start and r.end >= self.end:
            return [RangeMap(self.start, r.start - 1, self.offset), # Unmodified
                    RangeMap(r.start, self.end, self.offset + r.offset) # self + r
                    ]

        # "r" covers a part in the middle, but neither start or ends
        if r.start > self.start and r.end < self.end:
            # Returns 3 range maps, [U, M, U]
            return [
                RangeMap(self.start, r.start - 1, self.offset), # Unmodified
                RangeMap(r.start, r.end, self.offset + r.offset), # self + r
                RangeMap(r.end + 1, self.end, self.offset), # Unmodified
                ]

        # "r" covers fully the range
        if r.start <= self.start and r.end >= self.end:
            return [
                RangeMap(self.start, self.end, self.offset + r.offset)
            ]


        assert False, f"Should not get here, self: {self}, r: {r}"


    


@dataclass
class Map:
    name: str
    mappings: List[Mapping]

    def apply(self, i: int) -> int:
        for m in self.mappings:
            if m.inside(i):
                return m.apply(i)
        return i


def parse_seeds(seeds_data) -> List[int]:
    seeds = seeds_data.split(":")[1].strip().split()
    return [int(s) for s in seeds]


def parse_map(map_data) -> Map:
    # print(f"--{map_data}--")
    lines = map_data.split("\n")
    mappings = []
    name = lines[0]
    for l in lines[1:]:
        dest, source, range_ = l.split()
        mappings.append(
            Mapping(
                dest=int(dest), source=int(source), range_len=int(range_)
            )
        )

    return Map(name, mappings)


def parse(data) -> List[List[Mapping]]:
    chunks = data.split("\n\n")
    seeds = parse_seeds(chunks[0])
    map_data = chunks[1:]
    l = []
    for map in map_data:
        l.append(parse_map(map))

    return seeds, l

    


    


def day05(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    seeds, list_of_maps = parse(data)

    print(seeds)

    for m in list_of_maps:
        # print(m)
        seeds = [m.apply(s) for s in seeds]
        # print(seeds)

    result = min(seeds)
    if expected:
        assert result == expected, f"expected {expected}, got {result}"
    print(f"Result = {result}")

def parse_seeds_part2(seeds_data) -> List[RangeMap]:
    seeds = seeds_data.split(":")[1].strip().split()
    r = zip(seeds[::2], seeds[1::2])
    return [(RangeMap(int(s[0]), int(s[0]) + int(s[1]) - 1, offset=0)) for s in r]

def parse_part2(data):
    chunks = data.split("\n\n")
    seeds = parse_seeds_part2(chunks[0])
    map_data = chunks[1:]
    l = []
    for map in map_data:
        l.append([m.to_range_map() for m in parse_map(map).mappings])

    return seeds, l





def day05_part2(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    seeds, range_maps = parse_part2(data)

    print("Range Maps: \n", range_maps)

    for i, ranges in enumerate(range_maps):
        new_ranges = set()
        print(f"range {i}: {ranges}")
        for s in seeds:
            print("Seeds with offsets\n", seeds)
            for r in ranges:
                print("with range r\n", r)
                new_offsets = s.apply(r)
                if new_offsets[0] == s:
                    # Nothing changed, not the matching range
                    continue
                print("new offsets \n", new_offsets)
                new_ranges = new_ranges | set(new_offsets)
                break
                # nothing matched, keep seed for next round
            else:
                new_ranges.add(s)
        seeds = new_ranges
        print("After\n", seeds)


        

        

    print(f"Smallest location {min([s.start + s.offset for s in seeds])}")
    lowest_location = min([s.start + s.offset for s in seeds])
    #_, location_range = min([(s.offset, s) for s in seeds])


    #print(location_range)


    result = lowest_location
    if expected:
        assert result == expected, f"expected {expected}, got {result}"
    print(f"Result = {result}")

if __name__ == "__main__":
    #day05("day05_small.txt", expected=35)
    #day05("day05.txt")
    day05_part2("day05_small.txt", expected=46)
    day05_part2("day05.txt")


# After trying to list all the elements in the ranges, I'm thinking about an alternative approach.
# Applying many Map object is equivalent to a single "Map", with more mappings. 
# It should be efficient to find the lowest resutl based on that Map


# Part 2 a while after
# I tried eliminating all "invalid offsets". 
# 56558202
# 5010690169
#
# Once again, I've let myself stray too far from the visual interpretation and tried things without much directions.
#
