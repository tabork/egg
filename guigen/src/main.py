# from guigen.simulator import Simulator
# from guigen.generator import Generator
from ga.structures import UIRepr

from ga.ga import GA

import os
import random
import sys


if __name__ == "__main__":
    # simulator = Simulator(visualize=True)
    # simulator.run()

    # TODO Get results from args
    # simulator.output_results("output/test.json")

    # gen = Generator()

    # btns = gen.generate()
    # print(btns)

    # uirepr = UIRepr(btns)

    # print(uirepr)

    # uirepr[13] = 20

    # print()
    # print(uirepr)
    # # print(uirepr.matrix())
    # for i in uirepr:
    #     print(i)

    # if not os.path.isfile("output/results.csv"):

    ga = GA(results_file="output/results.csv")

    # for i in range(200):
    # print(f"ga: {list(ga.ga_step(0))}")

    ts = sys.maxsize
    while (g := ga.ga_step(ts)) is not None:
        ts = random.random()
        # print(g)

    ga.output_winner("output/winner.json")

    # t = "text2"

    # print(int(t == "text"))

    # t1 = TestClass(1)
    # print(t1.x)
    # t2 = type(t1)(2)
    # print(t2.x)

    # u = UIRepr(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    # print(u)
