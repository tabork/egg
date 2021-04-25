import pygame
import sys
from pygame.locals import *


class Window(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 0)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.process_events()
        pygame.display.flip()