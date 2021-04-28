"""Module for handling Chromosomes

Raises:
    ChromosomeException: If crossover is used before being defined
    ChromosomeException: If mutation is used before being defined
"""

__all__ = ["Chromosome", "ChromosomeException"]

import sys, random

from .utils import random_int


class ChromosomeException(Exception):
    """Generic exception for Chromosomes"""

    pass


class Chromosome:
    """Generic chromosome representation

    Raises:
        ChromosomeException: If crossover is used before being defined
        ChromosomeException: If mutation is used before being defined
    """

    def __init__(
        self,
        data=None,
        crossover_method=None,
        mutation_method=None,
        fitness_function=None,
        correction_function=None,
        fitness=None,
    ):
        """Initializes chromosome

        The data in a chromosome can be any form of chromosome,
        as long as it is compatible with the given selection,
        crossover, and mutation methods.

        Keyword Arguments:
            data                         -- Can be any representation of a chromosome. (default: {None})
            crossover_method             -- Function for performing crossover. (default: {None})
            mutation_method              -- Function for performing mutation. (default: {None})
            fitness_function             -- Function for calculating fitness. (default: {None})
            correction_function          -- Function for ensuring the chromosome is valid data (default: {None})
        """

        self.data = data
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self.fitness_function = fitness_function
        self.correction_function = correction_function
        if fitness_function is None and fitness is None:
            self.fitness = (
                sys.maxsize
            )  # If fitness function is not defined, set to maximum word size
        elif fitness is not None:
            self.fitness = fitness
        else:
            self.fitness = fitness_function(data)

    @classmethod
    def copy(cls, chrom):
        return cls(
            data=chrom.data,
            crossover_method=chrom.crossover_method,
            mutation_method=chrom.mutation_method,
            fitness_function=chrom.fitness_function,
            correction_function=chrom.correction_function,
            fitness=chrom.fitness,
        )

    def __repr__(self):
        """Representation of chromosome"""
        return f"Chromosome(fitness={self.fitness},\n\t\t{repr(self.data)}\n)"

    def calc_fitness(self):
        self.fitness = self.fitness_function(self.data)

    def set_crossover_method(self, crossover_method):
        """Sets the crossover method

        Arguments:
            crossover_method -- the new crossover method
        """
        self.crossover_method = crossover_method

    def set_mutation_method(self, mutation_method):
        """Sets the mutation method

        Arguments:
            mutation_method -- the new mutation method
        """
        self.mutation_method = mutation_method

    def __mul__(self, rhs):
        """Crossover operator

        Multiplication of two chromosomes is defined as the crossover operator.

        Arguments:
            rhs -- The other chromosome
        """

        if self.crossover_method is None:
            raise ChromosomeException("Crossover Method not defined.")
        child1_data, child2_data = self.crossover_method(self.data, rhs.data)
        return (
            Chromosome(
                child1_data,
                self.crossover_method,
                self.mutation_method,
                self.fitness_function,
                self.correction_function,
            ),
            Chromosome(
                child2_data,
                self.crossover_method,
                self.mutation_method,
                self.fitness_function,
                self.correction_function,
            ),
        )

    def correct(self):
        if self.correction_function is not None:
            return Chromosome(self.correction_function(self.data))

    def mutate(self):
        """Mutation operator

        Applies the mutation_method function
        """
        if self.mutation_method is None:
            raise ChromosomeException("Mutation Method not defined.")
        return Chromosome(self.mutation_method(self.data))

    def kick(self, max_attempts):
        old_fitness = self.fitness
        # for d in self.data:
        #     # if random.random() <= sub_kick_rate:
        attempts = 0
        while self.fitness >= old_fitness:
            r = random_int(len(self.data))
            d = self.data[r]
            for i in range(d.size):
                d.select_city(i)
                self.calc_fitness()
                if self.fitness < old_fitness:
                    break
                # print(f'old_fitness: {old_fitness}, new_fitness: {self.fitness}')
            attempts += 1
            if attempts > max_attempts:
                return True
        return False
