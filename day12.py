#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

from dataclasses import dataclass
from itertools import repeat

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
        if self.is_complete():
            # but really if we are checking for being invalid we should not be complete
            return not self.is_valid()
        # assume not complete, so a ? is remaining

        # check if any groups are longer than the valid part of the record
        valid_record = self.record[:self.record.find("?")]

        valid_groups = list(filter(None, [r.strip(".") for r in valid_record.strip(".").split(".")]))

        for vg, eg in zip(valid_groups, self.groups):
            if len(vg) > eg:
                return True

        # Maybe valid
        return False



def possible_arrangements(r: DamagedRecord) -> int:
    if r.is_complete():
        return 1 if r.is_valid() else 0

    if r.is_invalid():
        return 0

    possible_records = []
    for state in [".", "#"]:
        new_r = get_possible_arrangement(r, state)
        possible_records.append(new_r)

    return sum(possible_arrangements(r) for r in possible_records)
    



def get_possible_arrangement(r, state) -> DamagedRecord:
    assert not r.is_complete()
    return DamagedRecord(r.record.replace("?", state, 1), groups=r.groups)

def apply_group(r) -> DamagedRecord:
    next_group = r.groups[0]
    # what next? no clue


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

def parse_part2(data) -> List[DamagedRecord]:
    records = []
    for line in data.split("\n"):
        record, groups = line.split()
        parsed_groups = [int(g) for g in groups.split(",")]
        unfolded_groups = parsed_groups * 5
        records.append(DamagedRecord("?".join([record for i in range(5)]), unfolded_groups))

    return records

def day12_part2(filename, expected=None):

    with open(filename, "r") as f:
        data = f.read().strip()

    records = parse_part2(data)
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
    #day12_part2("day12_small.txt", expected=525152)
    #day12_part2("day12.txt")


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
# Even with pruning, it won't work.
#
# combinatorics time?
#
# Smarter possible arrangements?
# I think it's too late tonight.
