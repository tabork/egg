"""Module for the selection operators"""

__all__ = ["rank"]

from .utils import random_int

import random


def rank(chroms):
    """Gets a new population using ranking

    Arguments:
        chroms {List[Chromosome]} -- population
    """

    l = len(chroms)

    r = random_int(l)

    s = 1
    for i in range(l):
        if r <= s:
            return chroms[l - i - 1]
        s += i + 1

    return chroms[l - 1]


def tournament(chroms, alpha):
    l = len(chroms)

    c1 = random_int(l)
    c2 = random_int(l)
    ch1 = chroms[c1]
    ch2 = chroms[c2]
    if ch1.fitness < ch2.fitness:
        if random.random() < alpha:
            return ch1
        else:
            return ch2
    else:
        if random.random() > alpha:
            return ch2
        else:
            return ch1
