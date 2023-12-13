#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

from dataclasses import dataclass

@dataclass
class DamagedRecord:
    record: str
    groups: List[int]

    def is_complete(self):
        return all(c != "?" for c in self.record)


    def is_valid(self):
        """
        A record could still be incomplete but valid, but we can't know until all ? are replaced
        """
        damaged_groups = list(filter(None, [r.strip(".") for r in self.record.strip(".").split(".")]))
        if len(damaged_groups) != len(self.groups):
            return False
        for dg, expected_length in zip(damaged_groups, self.groups):
            if len(dg) != expected_length:
                return False
        return True

    def is_invalid(self) -> bool:
        """
        Look at the section without errors. If they contains groups impossible, that's an early invalid, don't check further
        """
        # Maybe too complex too soon
        pass




def possible_arrangements(r: DamagedRecord) -> int:
    if r.is_complete():
        return 1 if r.is_valid() else 0

    possible_records = []
    for state in [".", "#"]:
        new_r = get_possible_arrangement(r, state)
        possible_records.append(new_r)

    return sum(possible_arrangements(r) for r in possible_records)
    



def get_possible_arrangement(r, state) -> DamagedRecord:
    assert not r.is_complete()
    return DamagedRecord(r.record.replace("?", state, 1), groups=r.groups)




def parse(data) -> List[DamagedRecord]:
    records = []
    for line in data.split("\n"):
        record, groups = line.split()
        parsed_groups = [int(g) for g in groups.split(",")]
        records.append(DamagedRecord(record, parsed_groups))

    return records
                         


def day12(filename, expected=None):

    test_all_valid = """
#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1
    """.strip()


    test_records = parse(test_all_valid)
    for t in test_records:
        assert t.is_complete(), t
        assert t.is_valid(), t

    with open(filename, "r") as f:
        data = f.read().strip()

    records = parse(data)
    print(records)
    total_count = 0
    for r in records:
        count = possible_arrangements(r)
        print(r, count)
        total_count += count
    result = total_count
    if expected:
        assert result == expected, f"expected {expected}, got {result}"



    print(f"Result: {result}")

if __name__ == "__main__":
    day12("day12_small.txt", expected=21)
    day12("day12.txt")

# Start of problem:
# This one is going to require some clever use of combinatorics.
# I bet this won't work with brute force.

# But for part 1, I wonder if we could just get a list of permutations and filter them
# to get the number of arrangements
#
# Another way would be to split the "DamagedRecord" into smaller Damaged records, once we matched at least 1 group 
# with 100% certainty. Recursion into a smaller problem.
#
# I could split each record into "theoretical" record until no unknown remains, validate if that one is valid 
# and count the number that are valids
#
# It works! 23s so it could be faster, but it's simple enough
#
# Ouch, part 2 will need early pruning. And perhaps splitting of records?
