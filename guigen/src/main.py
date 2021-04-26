from guigen.simulator import Simulator

if __name__ == "__main__":
    simulator = Simulator(visualize=True)
    simulator.run()

    # TODO Get results from args
    # simulator.output_results("output/test.json")
