"""Module for handling populations"""

__all__ = ["PopulationException", "Population"]

import random, copy

from .chrom import Chromosome


class PopulationException(Exception):
    """Handles Exceptions for Populations"""

    pass


class Population:
    """Handles a Population"""

    def __init__(self, chroms=None, selection_method=None):
        """Initializes population

        Keyword Arguments:
            chroms           -- list of chromosomes (default: {None})
            selection_method -- selection method (default: {None})
        """

        self.chroms = chroms
        self.selection_method = selection_method
        if chroms is not None:
            self.chroms.sort(key=lambda c: c.fitness)

    def __repr__(self):
        return (
            f"Population([\n\t" + ",\n\t".join([repr(c) for c in self.chroms]) + "\n])"
        )

    def sort(self):
        if self.chroms is not None:
            self.chroms.sort(key=lambda c: c.fitness)

    def select(self):
        """Selects a chromosome based on selection method"""

        if self.selection_method is None:
            raise PopulationException("Selection Method is undefined.")

        return self.selection_method(self.chroms)

    def perform_selections(self):
        """Generates a new population with selection and crossover"""
        # print(self.chroms)
        chroms = [None] * len(self.chroms)
        chroms[0] = Chromosome.copy(self.chroms[0])
        # print(chroms[0])
        chroms[1] = Chromosome.copy(self.chroms[1])
        # print(chroms[1])
        for i in range(2, len(self.chroms), 2):
            child1, child2 = self.select() * self.select()
            # print(child1)
            chroms[i] = child1
            chroms[i + 1] = child2
            # print(type(chroms[i]))
            chroms[i].calc_fitness()
            chroms[i + 1].calc_fitness()
        return Population(chroms, self.selection_method)

    def perform_mutations(self, mutation_rate, on_elite=False):
        """Performs mutations on population

        Arguments:
            mutation_rate {float} -- probability of mutation
        """

        if not on_elite:
            for chrom in self.chroms[2:]:
                if random.random() <= mutation_rate:
                    chrom.mutate()
                    chrom.calc_fitness()
        else:
            for chrom in self.chroms:
                if random.random() <= mutation_rate:
                    chrom.mutate()
                    chrom.calc_fitness()

        self.chroms.sort(key=lambda c: c.fitness)

    def perform_corrections(self):
        for chrom in self.chroms:
            chrom.correct()

    def perform_kicks(self, kick_rate, max_attempts, on_elite=False):
        atmin = False
        if not on_elite:
            for chrom in self.chroms[2:]:
                if random.random() <= kick_rate:
                    atmin = chrom.kick(max_attempts)
        else:
            for chrom in self.chroms:
                if random.random() <= kick_rate:
                    atmin = chrom.kick(max_attempts)
        self.chroms.sort(key=lambda c: c.fitness)
        return atmin
