from guigen.simulator import Simulator

import os
import random
import sys
import time


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [output directory]\n")
        sys.exit(1)

    if not os.path.isdir(sys.argv[1]):
        print(f"Directory {sys.argv[1]} does not exist")
        sys.exit(1)

    timestr = time.strftime("%m%d%Y-%H%M%S")

    simulator = Simulator(visualize=True)
    simulator.run()

    simulator.output_results(os.path.join(sys.argv[1], f"results_{timestr}.json"))
