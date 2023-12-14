#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

def parse_rocks(p) -> List[List[int]]: 
    rocks = []
    for l in p.split("\n"):
        row = []
        for c in l:
            row.append(c)
        rocks.append(row)
    return rocks

def pretty_rocks(rocks):
    output = ""
    for r in rocks:
        output += "\n"
        output += "".join([c for c in r])
    return output

def transpose(rocks):
    "North becomes left/west, south becomes right"
    return list(map(list, zip(*rocks)))

def tilt_rocks_north(rocks):
    t_rocks = transpose(rocks)
    new_rocks = tilt_rocks_side(t_rocks, direction="left")
    return transpose(new_rocks)


def tilt_rocks_side(rocks, direction) -> List[List[str]]:
    if direction == "left":
        sorting_reverse = True
    else:
        sorting_reverse = False

    #print("Before tilted", direction)
    #print(pretty_rocks(rocks))
    new_rocks = []
    for row in rocks:
        # split rows by squares rows, then order the round rocks (reverse for left)
        split_rocks = "".join(row).split("#")
        sorted_splits = []
        for sr in split_rocks:
            print(sr)
            sorted_sr = "".join(sorted(sr, reverse=sorting_reverse))
            sorted_splits.append(sorted_sr)
        new_rocks.append(list("#".join(sorted_splits)))

    #print("Tilted", direction)
    #print(pretty_rocks(new_rocks))
    return new_rocks

def total_load(rocks):
    total_load = 0
    size = len(rocks)
    for i, row in enumerate(rocks):
        total_load += (size - i) * row.count("O")
    return total_load


def day14(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    rocks = parse_rocks(data)
    print(pretty_rocks(rocks))

    new_rocks = tilt_rocks_north(rocks)

    
    print(pretty_rocks(new_rocks))


    result = total_load(new_rocks)
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    day14("day14_small.txt", expected=136)
    day14("day14.txt")

# Great! Got part 1 in like 30 (maybe 40?) min!
# sorting the rocks really simplify this whole logic
