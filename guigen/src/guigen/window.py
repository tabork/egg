import pygame
import sys
from pygame.locals import *
from .button import Button, Shape


class Window(object):
    def __init__(self, width, height, fill):
        self.width = width
        self.height = height
        self.fill = pygame.Color(fill)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 0)
        self.buttons = []

    def set_buttons(self, buttons):
        self.buttons = buttons

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                xco, yco = event.pos
                for button in self.buttons:
                    button.click(xco, yco)

    def update(self):
        self.process_events()
        self.screen.fill(self.fill)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()