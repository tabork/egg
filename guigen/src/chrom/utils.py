"""Module for various utilities"""

__all__ = ["nextPowerOf2", "random_bitstring"]

import random

# from bitstring import BitArray


def nextPowerOf2(n):
    """Calculates the next power of 2, given n

    Taken from: https://www.geeksforgeeks.org/smallest-power-of-2-greater-than-or-equal-to-n/
    Method 3
    Complexity: O(lgn)

    Arguments:
        n -- The number for which to calculate the next power of 2

    Returns:
        int -- The next power of 2
    """
    p = 1
    if n and not (n & (n - 1)):
        return n

    while p < n:
        p <<= 1
    return p


def random_bitstring(l):
    return ["1" if random.random() < 0.5 else "0" for i in range(l)]
    # return BitArray(uint=r, length=l)


def random_int(*args):
    if len(args) == 2:
        beg, end = args
    elif len(args) == 1:
        beg = 0
        end = args[0]
    else:
        raise TypeError("Wrong number of arguments!")
    return int(random.random() * (end - beg) + beg)
