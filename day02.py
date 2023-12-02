#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class CubeSet:
    red: int
    blue: int
    green: int

@dataclass
class Game:
    """
    Max possible for each color
    """
    id: int
    red: int
    blue: int
    green: int

    def possible_cube_set(self, s: CubeSet) -> bool:
        return (
            self.red <= s.red and
            self.blue <= s.blue and
            self.green <= s.green 
                )

    def power(self) -> int:
        return self.red * self.blue * self.green
    



def parse(line) -> Game:
    game_id, bags = line.split(":")
    id = game_id[len("game"):]
    l = parse_bag(bags)
    max_red = max(map(lambda x: x.red, l))
    max_blue = max(map(lambda x: x.blue, l))
    max_green = max(map(lambda x: x.green, l))
    return Game(
        id=int(id),
        red=max_red,
        blue=max_blue,
        green=max_green,
    )


def parse_bag(bags) -> List[CubeSet]:
    sets = bags.split(";")
    l = []
    for s in sets:
        m = {color.split(" ")[1] : int(color.split(" ")[0]) for color in s.strip().split(", ")}
        l.append(CubeSet(red=m.get("red", 0),
            blue=m.get("blue", 0),
            green=m.get("green", 0),
                         ))
    return l


def day02(filename, expected=None):
    with open(filename, "r") as f:
        lines = f.read().split("\n")
    lines: List[str] = list(filter(None,lines))
    games = []
    
    for l in lines:
        game = parse(l)
        games.append(game)
    
    print(games)

    bag = CubeSet(red=12, blue=14, green=13)

    id_sum = sum([g.id for g in games if g.possible_cube_set(bag)])
    power_sum = sum([g.power() for g in games ])

    if expected:
        assert(expected == id_sum)

    print(id_sum)
    print(power_sum)


if __name__ == "__main__":
    day02("day02_small.txt", expected=8)
    day02("day02.txt")
