#

# from guigen.generator import Generator


from enum import Enum

import json
import os
import random
import sys
import time


class Mode(Enum):
    SIMULATION = 0
    GANN = 1
    VISUALIZE = 2
    ERROR = 3


MODE_MAP = {"sim": Mode.SIMULATION, "gann": Mode.GANN, "vis": Mode.VISUALIZE}


def get_dirs(argv, has_input=False):
    if has_input:
        if len(argv) != 4:
            print(f"Input and output directories required if running in 'gann' mode\n")
            sys.exit(1)

        output_dirs = [argv[2], argv[3]]
    else:
        if len(argv) != 3:
            print(f"Output directory required if running in 'sim' mode")
            sys.exit(1)

        output_dirs = [
            argv[2],
        ]

    for output_dir in output_dirs:
        if not os.path.isdir(output_dir):
            print(f"Directory {output_dir} does not exist")
            sys.exit(1)

    return output_dirs


def read_winner_as_buttons(filename):
    from guigen.button import Button

    with open(filename, "r") as f:
        d = json.load(f)

    btns = d["Buttons"]

    buttons = []
    for b in btns:
        buttons.append(
            Button(
                width=b["width"],
                height=b["height"],
                x=b["x"],
                y=b["y"],
                color=((b["fgr"], b["fgg"], b["fgb"]), (b["bgr"], b["bgg"], b["bgb"])),
                font=("Arial", 12),
                shape=b["shape"],
                text=("Goal" if b["goal"] == 1 else "Button"),
            )
        )

    return buttons


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            f"\nUsage: {sys.argv[0]} [mode] ('gann': input dir) ('sim' or 'gann': output dir) ('vis': input file)\n"
        )
        print(f"Example: {sys.argv[0]} gann training output\n")
        print(f"Example: {sys.argv[0]} sim training\n")
        print(f"Example: {sys.argv[0]} vis\n\n")
        sys.exit(1)

    if sys.argv[1] in MODE_MAP:
        mode = MODE_MAP[sys.argv[1]]
    else:
        mode = Mode.ERROR

    if mode == Mode.ERROR:
        print(f"Mode must be 'sim' 'gann' or 'vis'")
        sys.exit(1)

    timestr = time.strftime("%m%d%Y-%H%M%S")

    if mode == Mode.SIMULATION:
        output_dir = get_dirs(sys.argv)[0]

        # Needed import for sim
        from guigen.simulator import Simulator

        simulator = Simulator(visualize=True)
        simulator.run()

        simulator.output_results(
            os.path.join(output_dir, f"sim_results_{timestr}.json")
        )
    elif mode == Mode.GANN:
        dirs = get_dirs(sys.argv, True)

        # Needed imports for running the NN and GA
        from ga.ga import GA
        from nn.nn import NeuralNetwork

        input_dir = dirs[0]
        output_dir = dirs[1]

        NN = NeuralNetwork(input_dir)
        accuracy = NN.fit()
        print(f"Accuracy is estimated at {accuracy}")

        ts = sys.maxsize
        ga = GA(results_file=os.path.join(output_dir, f"ga_results_{timestr}.csv"))

        while (data := ga.ga_step(ts)) is not None:
            # print(data)
            ts = NN.predict(data)
            # print(ts)
            # print(ts)

        ga.output_winner(os.path.join(output_dir, f"ga_winner_{timestr}.json"))

        # gen = Generator()

        # while True:
        #     pred = NN.predict(list(UIRepr(buttons=gen.generate())))
        #     print(f"Prediction: {pred} s")
        #     time.sleep(3)
    else:
        if not os.path.isfile(sys.argv[2]):
            print(f"{sys.argv[2]} not found")
            sys.exit(1)

        from guigen.simulator import Window
        from guigen import settings

        window = Window(settings.WIDTH, settings.HEIGHT, settings.FILL)
        window.set_buttons(read_winner_as_buttons(sys.argv[2]))

        while True:
            window.update()
