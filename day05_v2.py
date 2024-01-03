#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Range:
    start: int
    end: int # inclusive
    def __post_init__(self):
        assert self.end >= self.start, f"Invalid! {self}"

@dataclass
class Mapping:
    start: int
    end: int #inclusive
    offset: int

    def __post_init__(self):
        assert self.start + self.offset >= 0, f"Invalid! {self}"


    def apply(self, r: Range) -> List[Range]:
        """
        A Mapping applying another will result in 1 or more mapping.
        The part r not covered by the self rangeMap is not returned
        """
        #print("Apply:", self, r)
        # no overlap, no changes
        if r.end < self.start or r.start > self.end:
            return []

        # the mapping covers the start but not the end of the range
        if self.start <= r.start and self.end < r.end:
            # Return modified first part and keept offset for the rest
            return [
                Range(r.start + self.offset, self.end + self.offset),
                Range(self.end + 1, r.end)
            ]

        # the mapping covers the end but not the start
        if r.start < self.start and r.end <= self.end:
            return [
                Range(r.start, self.start - 1), # Unmodified
                Range(self.start + self.offset, r.end + self.offset)
            ]


        # the mapping covers a part in the middle, but neither start or ends of the range
        if r.start < self.start and self.end < r.end:
            # Returns 3 range maps, [U, M, U]
            return [
                Range(r.start, self.start - 1), # Unmodified
                Range(self.start + self.offset, self.end + self.offset), # self + r
                Range(self.end + 1, r.end), # Unmodified
                ]

        # Mapping covers fully the range
        if self.start <= r.start and self.end >= r.end:
            return [
                Range(r.start + self.offset, r.end + self.offset)
            ]


        assert False, f"Should not get here, self: {self}, r: {r}"


@dataclass
class Map:
    name: str
    mappings: List[Mapping]

def parse(data, seed_func):
    chunks = data.split("\n\n")
    seeds_data = chunks[0]
    seeds = seed_func(seeds_data)
    maps = parse_maps(chunks[1:])
    return seeds, maps

def parse_maps(data) -> List[Map]:
    return [parse_map(chunk) for chunk in data]

def parse_map(data) -> Map:
    lines = data.split("\n")
    name = lines[0].split()[0]
    mappings = []
    for line in lines[1:]:
        mappings.append(parse_mapping(line))
    return Map(name, mappings)



def parse_mapping(data) -> Mapping:
    dest, source, range_ = data.split()
    start = int(source)
    end = int(source) + int(range_) - 1
    offset = int(dest) - int(source)
    return Mapping(start, end, offset)


def seeds_part1(data) -> List[Range]:
    seeds = data.split(":")[1].strip().split()
    return [Range(start=int(s), end=int(s)) for s in seeds]

def seeds_part2(data) -> List[Range]:
    seeds = data.split(":")[1].strip().split()
    r = zip(seeds[::2], seeds[1::2])
    return [Range(int(s[0]), int(s[0]) + int(s[1]) - 1) for s in r]


def day05(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    seeds, maps = parse(data, seeds_part1)
    print(f"Seeds: {sorted(seeds)},\n maps {maps}")

    current_ranges = seeds
    for map in maps:
        # Apply a set of mapping to get a new set of ranges
        new_ranges = set()
        print(f"Processing {map.name} mappings")
        for c_r in current_ranges:
            for mapping in map.mappings:
                ranges = mapping.apply(c_r)
                new_ranges = new_ranges | set(ranges)
                if ranges:
                    # a mapping was found, exit
                    break
            else:
                # if no mappings is applied, keep current range in set
                new_ranges.add(c_r)
        print(f"New ranges: {sorted(new_ranges)}")
        current_ranges = new_ranges

    result = sorted(new_ranges)[0].start
    if expected:
        assert result == expected, f"expected {expected}, got {result}"
    print(f"Result = {result}")

def day05_part2(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()
    seeds, maps = parse(data, seeds_part2)
    print(f"Seeds: {seeds},\n maps {maps}")
    current_ranges = seeds
    for map in maps:
        # Apply a set of mapping to get a new set of ranges
        new_ranges = set()
        print(f"Processing {map.name} mappings")
        for c_r in current_ranges:
            for mapping in map.mappings:
                ranges = mapping.apply(c_r)
                new_ranges = new_ranges | set(ranges)
                if ranges:
                    # a mapping was found, exit
                    break
            else:
                # if no mappings is applied, keep current range in set
                new_ranges.add(c_r)
        print(f"New ranges: {sorted(new_ranges)}")
        current_ranges = new_ranges

    result = sorted(new_ranges)[0].start
    if expected:
        assert result == expected, f"expected {expected}, got {result}"
    print(f"Result = {result}")

if __name__ == "__main__":
    day05("day05_small.txt", expected=35)
    day05("day05.txt")
    day05_part2("day05_small.txt", expected=46)
    day05_part2("day05.txt")
