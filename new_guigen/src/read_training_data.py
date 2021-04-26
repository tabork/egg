import json


def read_training_data(filename):
    with open(filename, "r") as f:
        d = json.load(f)

    trials = d["Trials"]
    param_mats = [
        [
            [
                b["x"],
                b["y"],
                b["width"],
                b["height"],
                b["colors"]["fg"]["r"],
                b["colors"]["fg"]["g"],
                b["colors"]["fg"]["b"],
                b["colors"]["bg"]["r"],
                b["colors"]["bg"]["g"],
                b["colors"]["bg"]["b"],
                b["shape"],
            ]
            for b in t["Buttons"]
        ]
        for t in trials
    ]

    times = [t["Time"] for t in trials]

    return (param_mats, times)


if __name__ == "__main__":
    print(read_training_data("output/test.json"))