#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

from dataclasses import dataclass

# Coordinates based on y going down, x going right
PIPES = {
    "|": [(0, -1), (0, 1) ],
    "-": [(1, 0), (-1, 0) ],
    "L": [(0, -1), (1, 0) ],
    "J": [(0, -1), (-1, 0) ],
    "7": [(0, 1), (-1, 0) ],
    "F": [(0, 1), (1, 0) ],
         }

@dataclass(frozen=True)
class Pipe:
    shape: str
    x: int
    y: int
    def next_pipe_pos(self) -> List[Tuple[int, int]]:
        "Possible pipes"
        if self.shape not in PIPES:
            return []
        offsets = PIPES[self.shape]
        return [(self.x + x, self.y + y) for x,y in offsets]





@dataclass
class Node:
    v: Pipe
    left: Pipe | None
    right: Pipe | None




@dataclass
class Grid:
    grid: List[List[Pipe]]
    start: Pipe

    def get_pipe(self, x, y) -> Pipe | None:
        if x < 0 or y < 0 or x >= len(self.grid[0]) or y >= len(self.grid):
            return None
        return self.grid[y][x]

    def find_connected_start(self) -> (Pipe, Pipe):
        directions = [
            (self.start.x, self.start.y - 1),
            (self.start.x, self.start.y + 1),
            (self.start.x - 1, self.start.y),
            (self.start.x + 1, self.start.y),
        ]
        pipes = []
        for d in directions:
            p = self.get_pipe(*d)
            if not p:
                continue
            for x, y in p.next_pipe_pos():
                if x == self.start.x and y == self.start.y:
                    pipes.append(p)


        return tuple(pipes)
                    

    def find_start_shape(self) -> str:
        p1, p2 = self.find_connected_start()

        # Get the original offset that would have been applied to start
        # start.x + ? = p1.x
        # ? = p1.x - start.x
        diff_1 = (p1.x - self.start.x,  p1.y - self.start.y)
        diff_2 = (p2.x - self.start.x,  p2.y - self.start.y)

        # find the shape with those offsets
        for shape, offsets in PIPES.items():
            if diff_1 in offsets and diff_2 in offsets:
                return shape

    def print_grid(self, loop: Set[Pipe]):
        #Debug function
        print("Grid:")
        count_i = 0
        for y, line in enumerate(self.grid):
            print_line = []
            for x, p in enumerate(line):
                if p in loop:
                    print_line.append(p.shape)
                else:
                    print_line.append("I" if self.is_in_loop(loop, p) else "O")

            print("".join(print_line))
            count_i += print_line.count("I")

        print(count_i)


    def is_in_loop(self, loop: Set[Pipe], p: Pipe) -> bool:
        # parse left to right, count the crossing of the loop
        crossing_pipes = ["L", "J", "|"]
        row = p.y
        crossing_count = 0
        for x in range(0, p.x + 1):
            tile = self.grid[row][x]
            # special case for start
            if tile == self.start:
                tile = Pipe(shape=self.find_start_shape(), x=tile.x, y=tile.y)

            if tile in loop and tile.shape in crossing_pipes:
                crossing_count += 1

        # An uneven count means it's in the loop
        return crossing_count % 2 == 1
                
                




            




def parse(data) -> Grid:
    grid = []
    for y, line in enumerate(data.split("\n")):
        row = []
        for x, c in enumerate(line):
            row.append(Pipe(shape=c, x=x, y=y))
        grid.append(row)

    start = find_start(grid)
    return Grid(grid, start)

def find_start(grid) -> Pipe:
    for line in grid:
        for p in line:
            if p.shape == "S":
                return p



def day10(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    grid = parse(data)


    print(grid)
    print("connected", grid.find_connected_start())
    explored = set([grid.start])
    print(explored)
    p1, p2 = grid.find_connected_start()
    step = 0
    while True:
        p1_next = [grid.get_pipe(*p) for p in p1.next_pipe_pos() if grid.get_pipe(*p) not in explored]
        p2_next = [grid.get_pipe(*p) for p in p2.next_pipe_pos() if grid.get_pipe(*p) not in explored]
        step += 1
        explored.add(p1)
        explored.add(p2)
        if p1 == p2:
            print("Reached the end, same pipe", p1, p2)
            break
        p1 = p1_next[0]
        p2 = p2_next[0]

    print(len(explored))
    
    # For each non-explored part of the grid, calculate the number of "crossing"
    # Only the follwing increase it





    result = step
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result part 1: {result}")

    shape = grid.find_start_shape()

    print(f"Shape start: {shape}")
    grid.print_grid(explored)



if __name__ == "__main__":
    day10("day10_small.txt", expected=8)
    day10("day10_part2_small.txt")
    #day10("day10.txt")

# This problem will need a tree or a graph. I expect the part 2 to need an efficient algo
#
# Part 2 wants to know the size of the inner loop
# I think counting the number of time we cross the "boundary" is a valid way to know if we are inside or not
# Ha, but the fact that the resolution is limited is a challenge.
# I think that if we represent each pipes in a higher resolution (like 3x3), we can solve this issue
# and use the ray casting point in polygon approach.
#
# For some reason, it seems like the only valid "crossing" are L, J and |. I don't get why it works but the tests works
