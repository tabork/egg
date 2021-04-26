import time
import json

from guigen import settings
from .window import Window
from .button import Button, Shape
from .generator import Generator


class Trial(object):
    def __init__(self, button_params):
        self.button_params = button_params

    def start(self):
        self.start_time = time.monotonic()

    def end(self):
        self.end_time = time.monotonic()

    def duration(self):
        return self.end_time - self.start_time


class Simulator(object):
    # trial_list = []
    def __init__(
        self,
        visualize=False,
        width=None,
        height=None,
        fill=None,
        num_trials=0,
        num_goals=None,
    ):
        self.visualize = visualize
        self.width = width if width is not None else settings.WIDTH
        self.height = height if height is not None else settings.HEIGHT
        self.fill = fill if fill is not None else settings.FILL
        self.num_trials = num_trials if num_trials > 0 else settings.TRIALS
        self.num_goals = num_goals if num_goals is not None else settings.GOALS
        self.generator = Generator()
        self.goals_found = []

        if self.visualize:
            self.window = Window(self.width, self.height, self.fill)

    def run(self):
        self.trials = []
        for trial in range(self.num_trials):
            button_params = self.generator.generate()

            self.current_trial = Trial(button_params)

            buttons = []
            for b in button_params:
                if b.text == "Goal":
                    buttons.append(
                        Button(
                            width=b.w,
                            height=b.h,
                            color=b.color,
                            font=("Arial", 12),
                            shape=b.shape,
                            x=b.x,
                            y=b.y,
                            text=b.text,
                            command=self.goal_clicked,
                        )
                    )
                else:
                    buttons.append(
                        Button(
                            width=b.w,
                            height=b.h,
                            color=b.color,
                            font=("Arial", 12),
                            shape=b.shape,
                            x=b.x,
                            y=b.y,
                            text=b.text,
                        )
                    )
            self.window.set_buttons(buttons)
            self.current_trial.start()
            self.goals_found = []
            while len(self.goals_found) < self.num_goals:
                self.window.update()
            self.current_trial.end()
            self.trials.append(self.current_trial)
        for t in self.trials:
            print(f"Duration: {t.duration()}, Params: {t.button_params}")

    def output_results(self, filename):
        d = []
        for trial in self.trials:
            params = trial.button_params
            btns = []

            for btn in params:
                color = btn.color
                fg = {"r": color[0][0], "g": color[0][1], "b": color[0][2]}
                bg = {"r": color[1][0], "g": color[1][1], "b": color[1][2]}
                btns.append(
                    {
                        "x": btn.x,
                        "y": btn.y,
                        "width": btn.w,
                        "height": btn.h,
                        "colors": {"fg": fg, "bg": bg},
                        "shape": btn.shape,
                    }
                )
            d.append({"Buttons": btns, "Time": trial.duration()})
        with open(filename, "w+") as f:
            json.dump({"Trials": d}, f)

    def goal_clicked(self, btn):
        if btn.idn not in self.goals_found:
            self.goals_found.append(btn.idn)