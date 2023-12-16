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
        #print(f"{i}: {hash(i)}")
        total += hash(i)


    result = total
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

def lens_power(box_num, box) -> int:
    total = 0
    for i, b in enumerate(box,1):
        _, focal_len = b
        total += box_num * i * focal_len

    return total

def focusing_power(boxes) -> int:
    total = 0
    for i, b in enumerate(boxes, 1):
        total += lens_power(i,b)
    return total



def day15_part2(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    init_seq = parse(data)
    boxes = [[] for i in range(256)]
    for i in init_seq:
        if "=" in i:
            label = i.split("=")[0]
            box_id = hash(label)
            value = int(i.split("=")[1])
            box = boxes[box_id]
            # Replace if exist
            for j, e in enumerate(box):
                if label == e[0]:
                    box[j] = (label, value)
                    break
            else:
                box.append((label, value))
        elif "-" in i:
            label = i.split("-")[0]
            box_id = hash(label)
            box = boxes[box_id]
            for j, e in enumerate(box):
                # is label in box?
                if label == e[0]:
                    # remove it
                    box.pop(j)
                    break
        else:
            assert False, "Should not append"

        # debugging
        print("After \"{i}\"", i)
        print([(f"Box {i}", b) for i, b in enumerate(boxes) if b])



    total = focusing_power(boxes)


    result = total
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    #day15("day15_small.txt", expected=1320)
    #day15("day15.txt")
    day15_part2("day15_small.txt", expected=145)
    day15_part2("day15.txt")

