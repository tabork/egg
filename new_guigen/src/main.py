from new_guigen.window import Window

if __name__ == "__main__":
    window = Window(1080, 720, (0, 0, 0))
    while True:
        window.update()