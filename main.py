#!/usr/bin/env python3
"""bfs-microfluid-test

perform a breadth-first search on every possible
output for a mixing graph
"""

from typing import Tuple
from typing import List
import pandas

MANTISSA_SIZE = 31
ONE = 1 << MANTISSA_SIZE


def fix_value(x: int) -> int:
    """fix_value

    Ensure that a value is within the expected range by capping it at a value of
    one using the fixed point representation defined for this program.
    """
    return ONE if x > ONE else x


def mix(x: int, y: int) -> int:
    """mix

    Takes two fixed-point values and returns their average.
    Any values larger than one are treated as a one.
    """
    x = fix_value(x)
    y = fix_value(y)
    if x == ONE and y == ONE:
        return ONE

    return (x + y) >> 1


def to_fraction(x: int) -> "Tuple[int, int]":
    """to_fraction

    Convert a fixed point value to a fraction.
    Return a tuple (numerator, denominator).
    """
    if x == 0:
        return (0, 1)
    if x >= ONE:
        return (1, 1)

    # find the last set bit
    index = 0
    while x & (1 << index) == 0 and index <= MANTISSA_SIZE:
        index += 1

    denominator = 1 << (MANTISSA_SIZE - index)
    numerator = x >> index
    return (numerator, denominator)


def compute_next(inp: List[int], i1: int, i2: int) -> List[int]:
    """compute_next

    get the next row of the mixing graph given two indices to be mixed
    """
    newlist = inp[:]
    res = mix(inp[i1], inp[i2])
    newlist[i1] = res
    newlist[i2] = res
    return newlist


def max_denominator(inp: List[int]) -> int:
    """max_denominator

    get the maximum denominator in the current row of the mixing graph
    """
    maxm = 0
    for i in inp:
        (_, d) = to_fraction(i)
        maxm = d if d > maxm else maxm
    return maxm


def main():  # pylint: disable=too-many-locals
    """main

    compute every possible output up to a given depth
    """
    init = tuple([0, 0, 0, ONE])
    result_set = {init: (init, 1)}

    curr = {init: True}
    nxt = {}

    for _ in range(20):
        for c in curr:
            i = len(c) - 1
            j = i - 1

            while i >= 0:  # go until i is out of range
                if j < 0:  # update the i pointer on overflow of j
                    i -= 1
                    j = i - 1

                res = compute_next(list(c), i, j)
                res.sort()
                c_next = tuple(res)
                md = max_denominator(res)
                if c_next not in result_set:
                    result_set |= {c_next: (c, md)}
                    nxt |= {c_next: True}
                else:
                    (_, tmp) = result_set[c_next]
                    if md < tmp:
                        result_set[c_next] = (c, md)
                        next |= {c_next: True}

                j -= 1

        curr = nxt
        nxt = {}

    data = []

    maximum_denominator_greater_than_solution = {}
    for result in result_set.keys():
        data_line = []
        (prevs, md) = result_set[result]
        for val in list(prevs):
            (n, d) = to_fraction(val)
            data_line.append(f"{n}/{d}")
        data_line.append("-->")
        for val in list(result):
            (n, d) = to_fraction(val)
            data_line.append(f"{n}/{d}")
        data.append(data_line)
        if md > max_denominator(result):
            maximum_denominator_greater_than_solution[result] = True

    df = pandas.DataFrame(data)
    print(df.to_string(header=False, index=False))

    print("Exceptional:")
    print(maximum_denominator_greater_than_solution)


if __name__ == "__main__":
    main()
