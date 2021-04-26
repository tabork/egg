# from new_guigen.window import Window
from guigen.simulator import Simulator

if __name__ == "__main__":
    # window = Window(1080, 720, (0, 0, 0))
    # while True:
    #     window.update()
    simulator = Simulator(visualize=True)
    simulator.run()

    # TODO Get results from args
    # simulator.output_results("output/test.json")
