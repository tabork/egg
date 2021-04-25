import tkinter as tk

from guigen.page import Page, PageManager
from guigen.button import Button, CLICKS
from guigen import settings


if __name__ == "__main__":
    window = tk.Tk()
    settings.LABEL = tk.Label(
        window,
        text=f"Find '{settings.GOAL}'. Current depth: 0. Clicks: {CLICKS}.",
        font=("Arial", 18),
    )
    col_start = max(settings.GRID_SIZE // 2 - 1, 0)
    # LABEL.grid(row=0, column=col_start, columnspan=3, sticky="we")
    settings.LABEL.pack(side="top", fill="x")
    container = tk.Frame(window)

    for i in range(settings.GRID_SIZE):
        container.columnconfigure(i, weight=1)
        container.rowconfigure(i, weight=1)

    container.pack(side="top", fill="both", expand=True)
    pm = PageManager(container)
    window.wm_geometry("600x400")
    window.mainloop()