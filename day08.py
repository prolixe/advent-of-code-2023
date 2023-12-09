#!/usr/bin/env python3

from typing import List, Set, Tuple, Collection, Dict

from itertools import cycle
from math import gcd
import math

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


def factorization(n):

    factors = []

    def get_factor(n):
        x_fixed = 2
        cycle_size = 2
        x = 2
        factor = 1

        while factor == 1:
            for count in range(cycle_size):
                if factor > 1: break
                x = (x * x + 1) % n
                factor = gcd(x - x_fixed, n)

            cycle_size *= 2
            x_fixed = x

        return factor

    while n > 1:
        next = get_factor(n)
        factors.append(next)
        n //= next

    return factors


def isPrime(number):
    if number == 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(number)) + 1, 2):
        if number % i == 0:
            return False

    return True
# An old function!
def getPrimeList(n):

    """Return a prime list up to the number n"""
    primeList = [2]  # since starting at 3 in range()
    for i in range(3, n, 2):  # since only uneven number are prime
        if isPrime(i):
            primeList.append(i)
    return primeList

def factorize(n, primes):
    """Return a list of prime factors
    """
    factors = []
    for p in primes:  # Get a prime from the list of prime
        if p * p > n:  # If the prime squared is bigger than the number, break
            break
        i = 0
        while n % p == 0:  # While it can be divided by the prime
            n //= p
            i += 1
        if i > 0:
            factors.append((p, i))  # append the prime and the number of loop
    if n > 1:
        factors.append((n, 1))
    return factors

def day08_part2(filename, expected=None):
    with open(filename, "r") as f:
        data = f.read().strip()

    direction, m = parse(data)
    print(direction, m)
    primes = getPrimeList(10000)
    positions = list( k for k in m.keys() if k[-1] == "A")
    step = 0
    step_per_positions = [0 for p in positions]
    for d in cycle(direction):
        print(f"Positions: {positions}")
        step += 1
        for index, position in enumerate(positions):
            left, right = m[position]
            print(f"direction: {d}, left: {left}, right: {right}")
            if d == "L":
                positions[index] = left
            elif d == "R":
                positions[index] = right
            else:
                exit(-1)



        print(f"Position: {position}")
        if all(p[-1] == "Z" for p in positions):
            break

        for i, p in enumerate(positions):
            if p[-1] == "Z" and step_per_positions[i] == 0:
                step_per_positions[i] = step

        if all(step_per_positions):
            print(step_per_positions)
            break


    factors = set()
    for s in step_per_positions:
        f_list = factorize(s, primes)
        print(f_list)
        for f in f_list:
            factors.add(f[0])
    print(factors)
        

    result = 1
    for s in factors:
        result *= s
    if expected:
        assert result == expected, f"expected {expected}, got {result}"

    print(f"Result: {result}")

if __name__ == "__main__":
    day08("day08_small.txt", expected=2)
    day08("day08_small2.txt", expected=6)
    day08("day08.txt")
    day08_part2("day08_small_part_2.txt", expected=6)
    day08_part2("day08.txt")

# Just following the positions is too long, need to find all the "cycle" and infer when they are going to all reach the same.
# So a sort of multiplication of all?
# Probably a smallest common divisor kind of thing?
