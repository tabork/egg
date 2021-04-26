from collections import namedtuple

ButtonRepr = namedtuple(
    "ButtonRepr", "x, y, width, height, fgr, fgg, fgb, bgr, bgg, bgb, shape"
)


class ButtonRepr(object):
    def __init__(self, x, y, width, height, fgr, fgg, fgb, bgr, bgg, bgb, shape):
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
        }

        self.button_repr_keys = list(self.button_repr.keys())
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

        self.button_repr[self.button_repr_keys[idx]] = val
        self.button_repr_values[idx] = val

    def __repr__(self):
        return repr(self.button_repr)

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
    def __init__(self, buttons):
        self.num_buttons = len(buttons)

        self.buttons = buttons
        self.button_reprs = []

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
                    btn.shape,
                )
            )

        self.btn_size = len(self.button_reprs[0])
        self.size = self.num_buttons * self.btn_size

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        if idx >= self.size or idx < 0:
            raise IndexError(f"{idx} out of range 0 to {self.size - 1}")

        btn_idx = idx // self.btn_size
        idx = idx % self.btn_size

        print(f"{btn_idx}, {idx}\n")

        return self.button_reprs[btn_idx][idx]

    def __setitem__(self, idx, val):
        if idx >= self.size or idx < 0:
            raise IndexError(f"{idx} out of range 0 to {self.size - 1}")

        btn_idx = idx // self.btn_size
        idx = idx % self.btn_size

        self.button_reprs[btn_idx][idx] = val

    def __repr__(self):
        return "\n".join([repr(btn) for btn in self.button_reprs])
