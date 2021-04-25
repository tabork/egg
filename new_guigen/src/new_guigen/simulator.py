import time

from new_guigen import settings
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

    def goal_clicked(self, btn):
        if btn.idn not in self.goals_found:
            self.goals_found.append(btn.idn)