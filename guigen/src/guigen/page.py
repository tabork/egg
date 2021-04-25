import tkinter as tk
import random

from guigen import settings
from guigen.button import CLICKS, Button


class Page(tk.Frame):
    cur_row = 0
    cur_col = 0

    def __init__(self, depth, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        for i in range(settings.GRID_SIZE):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        self.depth = depth

    def add_button(self, page, label):
        btn = Button(page, master=self, text=label, font=("Arial", 18))
        btn.grid(row=self.cur_row, column=self.cur_col, sticky="nsew")
        self.cur_col += 1
        if self.cur_col == settings.GRID_SIZE:
            self.cur_row += 1
            self.cur_col = 0

    def show(self):
        self.lift()


class WinPage(Page):
    def __init__(self, page, *args, **kwargs):
        super().__init__(-1, *args, **kwargs)

        for _ in range(settings.GRID_SIZE * settings.GRID_SIZE):
            self.add_button(page, "Restart")


class PageManager(object):
    pages = []
    win = None

    def __init__(self, container):
        labels = []
        for depth in range(settings.MAX_DEPTH):
            goal_on_page = False
            labels_d = []
            for _ in range(settings.GRID_SIZE):
                for _ in range(settings.GRID_SIZE):
                    if not goal_on_page and random.random() < settings.GOAL_PROBABILITY:
                        labels_d.append(settings.GOAL)
                        goal_on_page = True
                        goal_in_generation = True
                    else:
                        labels_d.append(random.choice(settings.CHARSET))
            if not goal_on_page and depth == settings.MAX_DEPTH - 1:
                l = random.randint(0, settings.GRID_SIZE * settings.GRID_SIZE)
                labels_d[l] = settings.GOAL
            page = Page(depth, master=container)
            # for label in labels:
            #     page.add_button(Button(page, master=prev_page, text=label))
            page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
            self.pages.append(page)
            labels.append(labels_d)
            print(depth)
            # self.generate_pages(container, depth, labels)

        self.win = WinPage(self.pages[0], master=container)
        self.win.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        for depth, labels_d in enumerate(labels):
            print(depth)
            for label in labels_d:
                self.pages[depth].add_button(
                    self.pages[(depth + 1) % settings.MAX_DEPTH]
                    if label != settings.GOAL
                    else self.win,
                    label,
                )

        self.pages[0].show()
