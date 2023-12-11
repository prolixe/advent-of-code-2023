#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

from dataclasses import dataclass

@dataclass(frozen=True)
class G: # Galaxy, but short name
    id: int
    x: int
    y: int



def parse(data) -> List[List[bool]]:
    grid = []
    for line in data.split("\n"):
        row = []
        for c in line:
            row.append(True if c == "#" else False)
        grid.append(row)
    return grid

def print_grid(grid):
    print("Grid:")
    for row in grid:
        print("".join("#" if c else "." for c in row ))


def expand_space(grid):
    new_grid = expand_row(grid)
    new_grid = list(map(list, zip(*new_grid)))
    new_grid = expand_row(new_grid)
    new_grid = list(map(list, zip(*new_grid)))
    return new_grid


def expand_row(grid):
    expanded_grid = []
    for row in grid:
        expanded_grid.append(row)
        if not any(row):
            expanded_grid.append(row)
    return expanded_grid

def find_galaxies(grid) -> List[G]:
    galaxies = []
    count = 1
    for y, row in enumerate(grid):
        for x, g in enumerate(row):
            if g:
                galaxies.append(G(id=count, x=x, y=y))
                count += 1
    return galaxies

def find_distance(g1, g2):
    # Return manhattan distance between the 2 galaxies
    # Might not be the best way to efficiently find all min distances, since it's O(n**2)
    # Edit: Nevermind, there is only 442 galaxies

    return abs(g1.x - g2.x) + abs(g1.y - g2.y)



def day11(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    grid = parse(data)

    print_grid(grid)
    grid = expand_space(grid)
    print_grid(grid)
    galaxies = find_galaxies(grid)
    print(galaxies)

    print("1 and 7: ", find_distance(galaxies[0], galaxies[6]))
    print("3 and 6: ", find_distance(galaxies[2], galaxies[5]))
    print("8 and 9: ", find_distance(galaxies[7], galaxies[8]))
    sum = 0
    for pos, g1 in enumerate(galaxies):
        for g2 in galaxies[pos:]:
            sum += find_distance(g1, g2)
        

    
    result = sum
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    day11("day11_small.txt", expected=374)
    day11("day11.txt")
