import pygame
from pygame.locals import *
from enum import IntEnum


SHAPES = 4


class Shape(IntEnum):
    CIRCLE = 0
    TRIANGLE = 1
    RECTANGLE = 2
    SQUARE = 3


class DrawFuncs:
    @staticmethod
    def draw_rect(screen, color, x, y, width, height):
        pygame.draw.rect(screen, color, Rect(x, y, width, height))

    @staticmethod
    def draw_circle(screen, color, x, y, width, _height):
        pygame.draw.circle(screen, color, (x + width / 2, y + width / 2), width / 2)

    @staticmethod
    def draw_triangle(screen, color, x, y, width, height):
        pygame.draw.polygon(
            screen,
            color,
            [(x + width / 2, y), (x + width, y + height), (x, y + height)],
        )


DRAW_MAP = {
    Shape.CIRCLE: DrawFuncs.draw_circle,
    Shape.TRIANGLE: DrawFuncs.draw_triangle,
    Shape.RECTANGLE: DrawFuncs.draw_rect,
    Shape.SQUARE: DrawFuncs.draw_rect,
}

CUR_ID = 0


class Button(object):
    def __init__(self, *, width, height, color, font, shape, x, y, text, command=None):
        global CUR_ID
        self.idn = CUR_ID
        CUR_ID += 1
        self.width = width
        self.height = height
        self.color = color
        self.bg_color = pygame.Color(color[0])
        self.fg_color = pygame.Color(color[1])
        self.font = font
        self.p_font = pygame.font.SysFont(self.font[0], self.font[1])
        self.shape = shape
        self.x = x
        self.y = y
        self.text = text
        self.rendered = self.p_font.render(self.text, True, self.fg_color)
        self.fw = self.rendered.get_width()
        self.fh = self.rendered.get_height()
        self.command = command

    def draw(self, screen):
        DRAW_MAP[self.shape](
            screen, self.bg_color, self.x, self.y, self.width, self.height
        )
        screen.blit(
            self.rendered,
            (self.x + (self.width - self.fw) / 2, self.y + (self.height - self.fh) / 2),
        )

    def in_button(self, x, y):
        return (
            x >= self.x
            and x <= self.x + self.width
            and y >= self.y
            and y <= self.y + self.height
        )

    def click(self, x, y):
        if self.command is not None and self.in_button(x, y):
            self.command(self)
