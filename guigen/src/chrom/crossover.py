"""Module for defining crossover methods"""

__all__ = ["uniform_crossover", "single_point_slice"]

import random

from .utils import nextPowerOf2, random_bitstring, random_int


def uniform_crossover(chrom1, chrom2, U=None):
    """Performs uniform crossover

    Generates a bitstring and crosses the chromosomes
    to produce 2 parents. If U[i] == 1, the child
    inherits from the corresponding number chromosome
    (i.e. child1 inherits from chrom1).
    Otherwise, the child inherits from the opposite parrent.

    Arguments:
        chrom1 -- Chromosome 1
        chrom2 -- Chromosome 2

    Keyword Arguments:
        U -- bit string for crossover (default: {None})

    Returns:
        (data, data) -- A tuple of children chromosomes
    """
    assert len(chrom1) == len(chrom2)

    l = len(chrom1)

    if U is None:
        U = random_bitstring(l)
        # print(U)

    child1 = [""] * l
    child2 = [""] * l

    for i in range(l):
        if U[i] == "1":
            child1[i] = chrom1[i]
            child2[i] = chrom2[i]
        else:
            child1[i] = chrom2[i]
            child2[i] = chrom1[i]
    return child1, child2


def single_point_slice(chrom1, chrom2, point=None):
    """Single point slice crossover

    Picks a point at random (or from given)
    and performs crossover where in front of
    point is inherited from chrom1 in child 1
    and from chrom2 in child 2, and the opposite
    for after point.

    Arguments:
        chrom1 -- Parent 1
        chrom2 -- Parent 2

    Keyword Arguments:
        point -- The point at which to perform crossover (default: {None})

    Returns:
        (data, data) -- Returns data to make two children
    """

    assert len(chrom1) == len(chrom2)

    l = len(chrom1)

    if point is None:
        point = random_int(l)

    child1 = chrom1[:point] + chrom2[point:]
    child2 = chrom2[:point] + chrom1[point:]

    return child1, child2
