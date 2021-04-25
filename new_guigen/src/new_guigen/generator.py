import random

from collections import namedtuple

from new_guigen import settings
from .button import Button, Shape, SHAPES

Paramaters = namedtuple("Parameters", ["x", "y", "w", "h", "color", "shape", "text"])

MIN_BUTTON_WIDTH = 55
MIN_BUTTON_HEIGHT = 20


class Generator(object):
    def __init__(
        self,
        width=None,
        height=None,
        fill=None,
        num_buttons=None,
        num_goals=None,
    ):
        self.width = width if width is not None else settings.WIDTH
        self.height = height if height is not None else settings.HEIGHT
        self.fill = fill if fill is not None else settings.FILL
        self.num_buttons = num_buttons if num_buttons is not None else settings.BUTTONS
        self.num_goals = num_goals if num_goals is not None else settings.GOALS

    def generate(self):
        button_params = []
        goals = set()

        while len(goals) != self.num_goals:
            goals.add(random.randrange(0, self.num_buttons))

        needs_generated = True

        while needs_generated:
            for i in range(self.num_buttons):
                overlap_fixed = False
                tries = 0
                while not overlap_fixed and tries < 10:
                    x = random.randrange(0, self.width - MIN_BUTTON_WIDTH)
                    y = random.randrange(0, self.height - MIN_BUTTON_HEIGHT)
                    shape = Shape(random.randrange(0, SHAPES))
                    w = random.randint(MIN_BUTTON_WIDTH, self.width - x)
                    if shape == Shape.SQUARE or shape == Shape.CIRCLE:
                        h = w
                    else:
                        h = random.randint(MIN_BUTTON_HEIGHT, self.height - y)
                    if x + w > self.width or y + h > self.height:
                        overlapping = True
                    else:
                        overlapping = False
                        for b in button_params:
                            if Generator.check_overlapping(
                                x, y, w, h, b.x, b.y, b.w, b.h
                            ):
                                overlapping = True
                                break
                    if overlapping:
                        # print("overlap")
                        # print(
                        #     f"{x}, {y}, {w}, {h}, {shape}, {self.width}, {self.height}"
                        # )
                        tries += 1
                        continue
                    # print("no overlap")
                    # print(f"{x + w}, {y + h}, {self.width}, {self.height}")
                    overlap_fixed = True
                    bg = Generator.rand_color()
                    fg = Generator.rand_color()
                    text = "Goal" if i in goals else "Button"
                    button_params.append(Paramaters(x, y, w, h, (bg, fg), shape, text))
                if not overlap_fixed:
                    break
            if len(button_params) != self.num_buttons:
                button_params = []
                continue
            needs_generated = False
        print(button_params)
        return button_params

    @staticmethod
    def check_overlapping(x1, y1, w1, h1, x2, y2, w2, h2):
        return not (
            (x1 + w1) < x2 or (x2 + w2) < x1 or (y1 + h1) < y2 or (y2 + h2) < y1
        )

    @staticmethod
    def rand_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
