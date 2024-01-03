#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

from dataclasses import dataclass

@dataclass
class DiggerStep:
    direction: str
    dist: int
    color: str

@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Terrain:
    grid: List[List[str]]
    points: Set[Point]
    def __str__(self):
        output = ""
        for r in self.grid:
            output += "\n"
            output += "".join([ c for c in r])
        return output
    @staticmethod
    def from_points( points: Set[Point]) -> "Terrain":
        min_x = min([p.x for p in points])
        min_y = min([p.y for p in points])
        max_x = max([p.x for p in points])
        max_y = max([p.y for p in points])

        grid = []

        # Have a an outside ring around the trench (for the -1 and +2)
        for y in range(min_y-1, max_y+2):
            row = []
            for x in range(min_x-1, max_x+2):
                row.append("#" if Point(x, y) in points else ".")
            grid.append(row)
        return Terrain(grid, points)

    def in_grid(self, point) -> bool:
        "Inside the grid"
        x, y = point.x, point.y
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)

    def lava_size(self):
        s = str(self)
        return s.count("#") + s.count(".")


DIR = [ (0, -1), (0, 1), (-1, 0), (1, 0) ]
def fill_points(grid: Terrain):
    # start with points sure to be outside
    points_to_fill = [Point(0,0)]
    while points_to_fill:
        p = points_to_fill.pop()

        x, y = p.x, p.y
        if grid.grid[y][x] == "#":
            continue
        grid.grid[y][x] = "O"
        for delta_x, delta_y in DIR:
            next_point = Point(x+delta_x, y+delta_y)
            if grid.in_grid(next_point) and grid.grid[next_point.y][next_point.x] == ".":
                points_to_fill.append(next_point)


def fill(grid: Terrain, points: Set[Point], p: Point, c: str) -> Terrain:
    # assuming the p point is inside unless the p point is part of the set
    x, y = p.x, p.y
    if p in points:
        return grid

    for delta_x, delta_y in DIR:
        next_point = Point(x+delta_x, y+delta_y)
        if grid.in_grid(next_point):
            grid = fill(grid, points, next_point, c)












def parse_line(line):
    direction, dist, color = line.split()
    return DiggerStep(direction, int(dist), color)

def parse(data):
    plan = []
    for line in data.split("\n"):
        ds = parse_line(line)
        plan.append(ds)
    return plan

def get_points(start_pos: Point, plan: List[DiggerStep]) -> List[Point]:
    all_points = [start_pos]
    for step in plan:
        start_pos, points = get_points_for_step(start_pos, step)
        all_points.extend(points)
    return all_points

def get_points_for_step(start_pos: Point, step: DiggerStep) -> Tuple[Point, List[Point]]:
    mapping = {
        "U": (0, -1),
        "D": (0, 1),
        "L": (-1, 0),
        "R": (1, 0),
    }
    
    points = []
    delta_x, delta_y = mapping[step.direction]
    for i in range(1, step.dist+1):
        # start at 1 because the start_pos is already dug
        points.append(Point(start_pos.x + (i*delta_x), start_pos.y + (i*delta_y)))

    # (Next pos, and all new holes dug)
    return (points[-1], points)


def day18(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    plan = parse(data)

    points = get_points(Point(0,0), plan)

    print(points)
    # Back to beginning
    assert(points[0] == points[-1])
    terrain = Terrain.from_points(set(points))
    print(terrain)

    fill_points(terrain)
    print(terrain)


    result = terrain.lava_size()
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    day18("day18_small.txt", expected=62)
    day18("day18.txt")

# Ok, so I sort of cheesed part 1 because I didn't want to fix the edge case for the filling algo, so I just filled the outside.
# Part 2 would be too huge to hold in memory, so to find the volume I'll have to find the general formula for a generic polygon.
#
# https://en.wikipedia.org/wiki/Shoelace_formula
#
# I came across that one before, but I didn't use it.
