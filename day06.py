#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

from dataclasses import dataclass

@dataclass
class Race():
    time: int
    distance: int

    def ways_to_wins(self) -> int:
        half = self.time // 2
        other_half = self.time - half


        ways = 0

        while half * other_half > self.distance:
            ways += 2 if half != other_half else 1 # in case it's equal like 15 ms charge for 30 ms time
            half -= 1 # most of the time it's the smaller half 15 // 2 -> 7
            other_half += 1

        return ways






def parse(data) -> List[Race]:
    table = []
    for line in data.split("\n"):
        label, rest = line.split(":")
        table.append(rest.split())
    

    t = list(zip(*table))
    return [ Race(int(r[0]), int(r[1])) for r in t]

def parse_part2(data) -> Race:
    table = []
    for line in data.split("\n"):
        label, rest = line.split(":")
        table.append(rest.split())

    print(table)

    return Race(int("".join(table[0])), int("".join(table[1])))




def day06(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    races = parse(data)
    print(races)
    mul_ways_to_win = 1
    for r in races:
        print(r.ways_to_wins())
        mul_ways_to_win *= r.ways_to_wins()


    result = mul_ways_to_win
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(result)

def day06_part2(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    race = parse_part2(data)
    print(race)


    result = race.ways_to_wins()
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(result)
if __name__ == "__main__":
    day06("day06_small.txt", expected=288)
    day06("day06.txt")
    day06_part2("day06_small.txt", expected=71503)
    day06_part2("day06.txt")

