import tkinter as tk

from guigen import settings

CLICKS = 0


class Button(tk.Button):
    def __init__(self, page, *args, **kwargs):
        self.page = page
        tk.Button.__init__(self, command=self.clicked, *args, **kwargs)

    def clicked(self):
        global CLICKS
        CLICKS += 1
        if self["text"] == settings.GOAL:
            settings.LABEL["text"] = f"Found goal! Clicks: {CLICKS}."
            CLICKS = -1
        else:
            settings.LABEL[
                "text"
            ] = f"Find '{settings.GOAL}'. Current depth: {self.page.depth}. Clicks: {CLICKS}."
        self.page.show()