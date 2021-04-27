import json
import pandas
import random
import sys

from ga import settings
from ga.structures import UIRepr

from chrom.population import Population
from chrom.chrom import Chromosome
from chrom.selection import rank
from chrom.crossover import uniform_crossover

from guigen.generator import Generator


class GA(object):
    def __init__(self, verbose=True, results_file=None):
        self.generator = Generator()
        self.population = Population(
            chroms=[
                Chromosome(
                    data=UIRepr(buttons=self.generator.generate()),
                    crossover_method=uniform_crossover,
                    mutation_method=self.ui_mutate,
                    fitness_function=self.ui_fitness,
                    correction_function=self.goal_correction,
                )
                for _ in range(settings.POPULATION_SIZE)
            ],
            selection_method=rank,
        )

        self.last_iteration_set = 0
        self.least = sys.maxsize
        self.least_iteration = 0
        self.total_iterations = 0
        self.current_iteration = 0
        self.converged = False
        self.verbose = True
        self.results_file = results_file
        self.current_index = 0

        self.df = pandas.DataFrame(
            {"Generation": [], "Fitness": [], "Min Fitness": [], "Min Iteration": []}
        )

        if self.results_file is not None:
            self.datas = {
                "Generation": [],
                "Fitness": [],
                "Min Fitness": [],
                "Min Iteration": [],
            }

    def ga_step(self, last_timestamp):
        print(self.current_iteration)
        if self.current_index == 0 and self.current_iteration != 0:
            self.last_iteration_set = self.population.chroms[0].fitness
            if self.verbose:
                if self.current_iteration % 1000 == 0:
                    print(
                        f"Iteration: {self.current_iteration}, Fitness: {self.population.chroms[0].fitness}, Minimum: {self.least}, Min Iteration: {self.least_iteration}"
                    )
            # print("Performing selections")
            self.population = self.population.perform_selections()
            fitness = self.population.chroms[0].fitness
            if fitness < self.least:
                self.least = self.population.chroms[0].fitness
                self.least_iteration = self.current_iteration
            if self.current_iteration % 50 == 0:
                if self.results_file is not None:
                    self.datas["Generation"].append(self.current_iteration)
                    self.datas["Fitness"].append(fitness)
                    self.datas["Min Fitness"].append(self.least)
                    self.datas["Min Iteration"].append(self.least_iteration)
            # print("Perfomring mutations")
            self.population.perform_mutations(settings.MUTATION_RATE)
            self.population.perform_corrections()
        elif self.current_index == settings.POPULATION_SIZE - 1:
            self.current_iteration += 1

        if not (self.current_index == 0 and self.current_iteration == 0):
            c = self.population.chroms[
                (self.current_index - 1) % settings.POPULATION_SIZE
            ]
            c.data.set_timestamp(last_timestamp)
            c.calc_fitness()

        if self.current_iteration == settings.MAX_ITERATIONS:
            if self.results_file is not None:
                # print(datas)
                fitness = self.population.chroms[0].fitness
                self.datas["Generation"].append(self.current_iteration)
                self.datas["Fitness"].append(fitness)
                self.datas["Min Fitness"].append(self.least)
                self.datas["Min Iteration"].append(self.least_iteration)
                df = pandas.DataFrame(self.datas)
                # print(df)
                df.to_csv(
                    self.results_file,
                    header=True,
                    index=False,
                )
            return None

        self.current_index = (self.current_index + 1) % settings.POPULATION_SIZE

        return self.population.chroms[
            (self.current_index - 1) % settings.POPULATION_SIZE
        ].data

    def output_winner(self, filename=None):
        if filename is None:
            print(f"Winner:\n{self.population.chroms[0].data}")
        else:
            with open(filename, "w+") as f:
                json.dump({"Buttons": self.population.chroms[0].data.output()}, f)

    def goal_correction(self, data):
        data.goal_correction()
        return data

    def ui_mutate(self, data):
        for i in range(len(data)):
            if random.random() < settings.SUB_MUTATION_RATE:
                data[i] = self.generator.get_random(i, data)
        return data

    def ui_fitness(self, data):
        return data.timestamp
