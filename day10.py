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
        print(self.start)
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
    step = 1
    while True:
        p1_next = [grid.get_pipe(*p) for p in p1.next_pipe_pos() if grid.get_pipe(*p) not in explored]
        p2_next = [grid.get_pipe(*p) for p in p2.next_pipe_pos() if grid.get_pipe(*p) not in explored]
        if not p1_next or not p2_next:
            # reached the end!
            print("Reached the end", p1, p2)
            break
        if p1 == p2:
            print("Reached the end, same pipe", p1, p2)
            break


        explored.add(p1)
        explored.add(p2)

        p1 = p1_next[0]
        p2 = p2_next[0]

        step += 1






    result = step
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    day10("day10_small.txt", expected=8)
    day10("day10.txt")

# This problem will need a tree or a graph. I expect the part 2 to need an efficient algo
