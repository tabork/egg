# from new_guigen.window import Window
from new_guigen.simulator import Simulator

if __name__ == "__main__":
    # window = Window(1080, 720, (0, 0, 0))
    # while True:
    #     window.update()
    simulator = Simulator(visualize=True)
    simulator.run()
    simulator.output_results("output/test.json")