#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

def dayXX(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read()

    result = 0
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    dayXX("dayXX_small.txt")
    dayXX("dayXX.txt")
