#!/usr/bin/env python3


def dayXX(filename):
    with open(filename, "r") as f:
        data = f.readlines()

if __name__ == "__main__":
    dayXX("dayXX.txt")
    dayXX("dayXX_small.txt")
