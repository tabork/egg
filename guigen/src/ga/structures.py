import random
import sys

from collections import namedtuple

from guigen.button import Button
from guigen import settings

ButtonRepr = namedtuple(
    "ButtonRepr", "x, y, width, height, fgr, fgg, fgb, bgr, bgg, bgb, shape"
)


class ButtonRepr(object):
    NUM_FIELDS = 12
    KEYS = [
        "x",
        "y",
        "width",
        "height",
        "fgr",
        "fgg",
        "fgb",
        "bgr",
        "bgg",
        "bgb",
        "shape",
        "goal",
    ]

    def __init__(self, x, y, width, height, fgr, fgg, fgb, bgr, bgg, bgb, shape, goal):
        self.button_repr = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "fgr": fgr,
            "fgg": fgg,
            "fgb": fgb,
            "bgr": bgr,
            "bgg": bgg,
            "bgb": bgb,
            "shape": shape,
            "goal": goal,
        }

        self.button_repr_values = list(self.button_repr.values())

    def __len__(self):
        return len(self.button_repr_keys)

    def __getitem__(self, idx):
        if idx >= len(self.button_repr_values) or idx < 0:
            raise IndexError(
                f"{idx} out of range 0 to {len(self.button_repr_values) - 1}"
            )

        return self.button_repr_values[idx]

    def __setitem__(self, idx, val):
        if idx >= len(self.button_repr_values) or idx < 0:
            raise IndexError(
                f"{idx} out of range 0 to {len(self.button_repr_values) - 1}"
            )

        self.button_repr[ButtonRepr.KEYS[idx]] = val
        self.button_repr_values[idx] = val

    def __repr__(self):
        return repr(self.button_repr)

    def __iter__(self):
        for elem in self.button_repr_values:
            yield elem

    def get_by_key(self, key):
        if key not in self.button_repr:
            raise KeyError(f"{key} not in ButtonRepr")

        return self.button_repr[key]

    def set_by_key(self, key, val):
        if key not in self.button_repr:
            raise KeyError(f"{key} not in ButtonRepr and adding keys is not allowed")

        self.button_repr[key] = val
        self.button_repr_values = list(self.button_repr.values())


class UIRepr(object):
    def __init__(self, *args, buttons=None):
        self.button_reprs = []
        if buttons is None:
            for i in range(0, len(args), ButtonRepr.NUM_FIELDS):
                self.button_reprs.append(
                    ButtonRepr(*args[i : i + ButtonRepr.NUM_FIELDS])
                )

            self.num_buttons = len(self.button_reprs)
        else:
            self.num_buttons = len(buttons)

            self.buttons = buttons

            for btn in buttons:
                fg = btn.color[0]
                bg = btn.color[1]
                self.button_reprs.append(
                    ButtonRepr(
                        btn.x,
                        btn.y,
                        btn.w,
                        btn.h,
                        fg[0],
                        fg[1],
                        fg[2],
                        bg[0],
                        bg[1],
                        bg[2],
                        int(btn.shape),
                        int(btn.text == "Goal"),
                    )
                )

        self.size = self.num_buttons * ButtonRepr.NUM_FIELDS

        self.timestamp = sys.maxsize

    def matrix(self):
        return [list(btn) for btn in self.button_reprs]

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_key(self, idx):
        return ButtonRepr.KEYS[idx % ButtonRepr.NUM_FIELDS]

    def get_index(self, key):
        return ButtonRepr.KEYS.index(key)

    def get_button(self, idx):
        return self.button_reprs[idx // ButtonRepr.NUM_FIELDS]

    def goal_correction(self):
        goal_index = self.get_index("goal")
        goal_count = sum(
            self[i] for i in range(goal_index, self.size, ButtonRepr.NUM_FIELDS)
        )

        if goal_count != settings.GOALS:
            for i in range(goal_index, self.size, ButtonRepr.NUM_FIELDS):
                if goal_count < settings.GOALS:
                    if self[i] == 0:
                        if random.random() < 0.5:
                            self[i] = 1
                            goal_count += 1
                elif goal_count > settings.GOALS:
                    if self[i] == 1:
                        if random.random() < 0.5:
                            self[i] = 0
                            goal_count -= 1
                else:
                    break

    def output(self):
        return [b.button_repr for b in self.button_reprs]

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        if idx >= self.size or idx < 0:
            raise IndexError(f"{idx} out of range 0 to {self.size - 1}")

        btn_idx = idx // ButtonRepr.NUM_FIELDS
        idx = idx % ButtonRepr.NUM_FIELDS

        # print(f"{btn_idx}, {idx}\n")

        return self.button_reprs[btn_idx][idx]

    def __setitem__(self, idx, val):
        if idx >= self.size or idx < 0:
            raise IndexError(f"{idx} out of range 0 to {self.size - 1}")

        btn_idx = idx // ButtonRepr.NUM_FIELDS
        idx = idx % ButtonRepr.NUM_FIELDS

        self.button_reprs[btn_idx][idx] = val

    def __repr__(self):
        return "\n".join([repr(btn) for btn in self.button_reprs])

    def __iter__(self):
        for oelem in self.button_reprs:
            for elem in oelem:
                yield elem
