#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

def parse(data) -> List[str]:
    return data.split(",")

def hash(input) -> int:
    current_val = 0
    for i in input:
        current_val += ord(i)
        current_val *= 17
        current_val %= 256
    return current_val



def day15(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    init_seq = parse(data)

    total = 0
    for i in init_seq:
        total += hash(i)


    result = total
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    day15("day15_small.txt", expected=1320)
    day15("day15.txt")
