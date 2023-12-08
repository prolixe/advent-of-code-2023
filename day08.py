#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

from itertools import cycle

def parse(data) -> Tuple[str, Dict[str, Tuple[str, str]]]:
    direction, rest = data.split("\n\n")
    m = {}
    for l in rest.split("\n"):
        key, value = l.split(" = ")
        # remove parens
        value = value[1:len(value) - 1]
        left, right = value.split(",")
        m[key] = (left.strip(), right.strip())
    return direction, m
        

def day08(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    direction, m = parse(data)
    print(direction, m)
    position = "AAA"
    step = 0
    for d in cycle(direction):
        print(f"Position: {position}")
        step += 1
        left, right = m[position]
        print(f"direction: {d}, left: {left}, right: {right}")
        if d == "L":
            position = left


        elif d == "R":

            position = right
        else:
            exit(-1)

        print(f"Position: {position}")
        if position == "ZZZ":
            break


    result = step
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    day08("day08_small.txt", expected=2)
    day08("day08_small2.txt", expected=6)
    day08("day08.txt")
