#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

from dataclasses import dataclass, field
from enum import Enum, auto
import copy
import time

EMPTY = "."
RIGHT_TO_UP = "/"
RIGHT_TO_DOWN = "\\"
SPLITTER_PIPE = "|"
SPLITTER_DASH = "-"


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

@dataclass(frozen=True)
class Beam:
    direction: Direction
    x: int
    y: int

    
    def next_position(self) -> "Beam":
        # Given the beam direction and position, where does it goes next?
        mapping = {
            Direction.RIGHT: (1,0),
            Direction.UP: (0, -1),
            Direction.LEFT: (-1, 0),
            Direction.DOWN: (0, 1),
        }
        x, y = mapping[self.direction]
        return Beam(self.direction, self.x + x, self.y + y)

@dataclass
class Tile:
    type: str
    energized: int = 0
    visited_beams: Set[Beam] = field(default_factory=set)

    def __str__(self):
        if self.energized > 0:
            return f"{min(self.energized,9)}"
        return self.type

    def process_beam(self, beam) -> List[Beam]:
        # Process beam and return a list of new beam, moved to the next position
        
        # If the tile was visited by a beam from the same location and the same directions
        # do not process it to avoid loops:
        if beam in self.visited_beams:
            return []
        self.visited_beams.add(beam)

        

        self.energized += 1

        directions: List[Direction] = []
        if self.type == EMPTY:
            # Same direction, with new position
            directions = [beam.direction]
        elif self.type == RIGHT_TO_UP:
            mapping = {
                Direction.RIGHT: Direction.UP,
                Direction.UP: Direction.RIGHT,
                Direction.LEFT: Direction.DOWN,
                Direction.DOWN: Direction.LEFT,
            }
            directions = [mapping[beam.direction]]
        elif self.type == RIGHT_TO_DOWN:
            mapping = {
                Direction.RIGHT: Direction.DOWN,
                Direction.UP: Direction.LEFT,
                Direction.LEFT: Direction.UP,
                Direction.DOWN: Direction.RIGHT,
            }
            directions = [mapping[beam.direction]]
        elif self.type == SPLITTER_PIPE:
            if beam.direction in [Direction.LEFT, Direction.RIGHT]:
                directions = [Direction.UP, Direction.DOWN]
            elif beam.direction in [Direction.UP, Direction.DOWN]:
                directions = [beam.direction]
            else:
                assert False, "Should not reach here"

        elif self.type == SPLITTER_DASH:
            if beam.direction in [Direction.LEFT, Direction.RIGHT]:
                directions = [beam.direction]
            elif beam.direction in [Direction.UP, Direction.DOWN]:
                directions = [Direction.LEFT, Direction.RIGHT]
            else:
                assert False, "Should not reach here"
        if not directions:
            assert False, "Should not reach here"

        beams = [Beam(direction=d, x=beam.x, y=beam.y).next_position() for d in directions]
        return beams

@dataclass
class Grid:
    grid: List[List[Tile]]

    def __str__(self):
        output = ""
        for r in self.grid:
            output += "\n"
            output += "".join([str(c) for c in r])
        return output

    def energized_count(self):
        total = 0
        for row in self.grid:
            for t in row:
                total += 1 if t.energized else 0
        return total


        

    def get_tile(self, x, y) -> Tile | None:
        # Not a copy
        if y < 0 or y >= len(self.grid):
            return None
        if x < 0 or x >= len(self.grid[0]):
            return None
        return self.grid[y][x]

    def process_beam(self, beam) -> List[Beam]:
        # apply beam effect on tile
        # return beam or beams resulting from tile.
        # Let's be clear about the steps.
        # A beam start unapplied to a tile.
        # It's then "processed", which apply energize the tile (increase the count)
        # and depending on the time, new beams are generated, with the next position they should have.
        tile = self.get_tile(beam.x, beam.y)
        if not tile:
            # Beam left the grid
            # print("In grid: process_beam, no tile found",beam)
            return []

        new_beams = tile.process_beam(beam)
        #print("In grid: process_beam", new_beams)

        return new_beams
        
        


def parse(data) -> Grid:
    grid = []
    for l in data.split("\n"):
        row = []
        for c in l:
            row.append(Tile(type=c))
        grid.append(row)
    return Grid(grid=grid)


def day16(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    grid = parse(data)

    # Top left, heading to the right
    start_beam = Beam(direction=Direction.RIGHT, x=0, y=0)

    beams = [start_beam]

    cycle_unchanged = 0
    last_energized_count = 0
    while beams:
        # take one beam
        beam = beams.pop()
        new_beams = grid.process_beam(beam)
        # show the grid while solving it
        #print(grid)
        #print(new_beams)
        # Make sure to process the new beams first
        new_beams.extend(beams)
        beams = new_beams
        time.sleep(0.01)
        if grid.energized_count() == last_energized_count:
            cycle_unchanged += 1
        else:
            last_energized_count = grid.energized_count()
            cycle_unchanged = 0

        #print("Cycle", cycle_unchanged)
        if cycle_unchanged > 100:
            print(f"No change detected for {cycle_unchanged} cycle, exiting")
            break


    result = grid.energized_count()
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

def count_energized(grid, start_beam) -> int:
    beams = [start_beam]

    cycle_unchanged = 0
    last_energized_count = 0
    while beams:
        # take one beam
        beam = beams.pop()
        new_beams = grid.process_beam(beam)
        # show the grid while solving it
        # print(grid)
        #print(new_beams)
        # Make sure to process the new beams first
        new_beams.extend(beams)
        beams = new_beams
        #time.sleep(1)
        if grid.energized_count() == last_energized_count:
            cycle_unchanged += 1
        else:
            last_energized_count = grid.energized_count()
            cycle_unchanged = 0

        #print("Cycle", cycle_unchanged)
        if cycle_unchanged > 100:
            # print(f"No change detected for {cycle_unchanged} cycle, exiting")
            break

    result = grid.energized_count()
    return result

def day16_part2(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    grid = parse(data)

    right_beams = [Beam(Direction.RIGHT, x=0,y=y) for y in range(0, len(grid.grid))]
    left_beams = [Beam(Direction.LEFT, x=len(grid.grid[0])-1,y=y) for y in range(0, len(grid.grid))]
    up_beams = [Beam(Direction.UP, x=x,y=len(grid.grid)-1) for x in range(0, len(grid.grid[0]))]
    down_beams = [Beam(Direction.DOWN, x=x,y=0) for x in range(0, len(grid.grid[0]))]
    start_beams = right_beams + left_beams + up_beams + down_beams


    max_energized = 0
    max_start_beam = None
    for b in start_beams:
        copied_grid = copy.deepcopy(grid)
        energized_count = count_energized(copied_grid, b)
        
        if energized_count > max_energized:
            max_energized = energized_count
            max_start_beam = b

    result = max_energized
    print("Max start beam", max_start_beam)

    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    day16("day16_small.txt", expected=46)
    day16("day16.txt")
    day16_part2("day16_small.txt", expected=51)
    day16_part2("day16.txt")
