#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

def parse(data) -> List[List[int]]:
    return [[int(i) for i in l.split()] for l in data.split("\n")]
        
def diff_each_step(seq: List[int]) -> List[int]:
    return [seq[i+1] - seq[i] for i in range(len(seq)-1)]

def predict_next_elem(seq: List[int]) -> int:
    if all(s == 0 for s in seq):
        return 0
    next_elem = seq[-1] + predict_next_elem(diff_each_step(seq))

    #print(seq, next_elem)
    return next_elem



def day09(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    sequences = parse(data)

    print(sequences)
    sum_next_elems = 0
    for s in sequences:
        next_elem = predict_next_elem(s)
        print(next_elem)
        sum_next_elems += next_elem

    result = sum_next_elems
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    day09("day09_small.txt", expected=114)
    day09("day09.txt")
