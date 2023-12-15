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
    new_rocks = tilt_rocks_side(t_rocks, direction="west")
    return transpose(new_rocks)

def tilt_rocks_south(rocks):
    t_rocks = transpose(rocks)
    new_rocks = tilt_rocks_side(t_rocks, direction="east")
    return transpose(new_rocks)

def tilt_rocks_side(rocks, direction) -> List[List[str]]:
    if direction == "west":
        sorting_reverse = True
    elif direction == "east":
        sorting_reverse = False
    else:
        assert False, f"Direction bad: {direction}"

    #print("Before tilted", direction)
    #print(pretty_rocks(rocks))
    new_rocks = []
    for row in rocks:
        # split rows by squares rows, then order the round rocks (reverse for left)
        split_rocks = "".join(row).split("#")
        sorted_splits = []
        for sr in split_rocks:
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

def cycle(rocks):
    rocks = tilt_rocks_north(rocks)
    rocks = tilt_rocks_side(rocks, direction="west")
    rocks = tilt_rocks_south(rocks)
    rocks = tilt_rocks_side(rocks, direction="east")
    return tuple(tuple(row) for row in rocks)

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

def load_at_cycle(rocks, count) -> int:
    "Brute force"
    for i in range(1, count+1):
        rocks = cycle(rocks)

    return total_load(rocks)
    

def load_at_cycle_prediction(rocks, count) -> int:
    "Find a cycle, extrapolate"
    cycle_tl = dict()
    rocks_patterns = [None] # So offset logic works
    for i in range(1, count+1):
        rocks = cycle(rocks)
        if rocks in cycle_tl:
            # Reached a known iteration!
            break
        cycle_tl[rocks] = i
        rocks_patterns.append(rocks)
    else:
        assert False, "Need to break, didn't find a pattern"

    interval = i - cycle_tl[rocks] 
    start = cycle_tl[rocks]
    # cut rock pattern at start of "cycle"
    rocks_patterns = rocks_patterns[start:]
    assert len(rocks_patterns) == interval
    position = (count - start) % interval 

    return total_load(rocks_patterns[position])

def day14_part2(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    rocks = parse_rocks(data)
    #print(pretty_rocks(rocks))

    # sanity check for prediction algo, only works for day14_small
    #for i in range(10, 100):
    #    bf = load_at_cycle(rocks, i)
    #    cp = load_at_cycle_prediction(rocks, i)
    #    assert bf == cp, f"Prediction algo wrong: got {cp}, expected {bf}"


    result = load_at_cycle_prediction(rocks, 10**9)
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    #day14("day14_small.txt", expected=136)
    #day14("day14.txt")
    day14_part2("day14_small.txt", expected=64)
    day14_part2("day14.txt")

# Great! Got part 1 in like 30 (maybe 40?) min!
# sorting the rocks really simplify this whole logic
#
# Part 2:
# I knew it would involve all directions! But 10**9 cycles! There better be a stable pattern here.
#
