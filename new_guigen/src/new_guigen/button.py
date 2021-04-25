import pygame
from pygame.locals import *
from enum import Enum


class Shape(Enum):
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
        pygame.draw.circle(screen, color, (x, y), width / 2)

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


class Button(object):
    def __init__(
        self,
        *,
        width,
        height,
        color,
        font,
        shape,
        x,
        y,
        text,
        command=lambda: print("Clicked")
    ):
        self.width = width
        self.height = height
        self.color = color
        self.p_color = pygame.Color(color)
        self.font = font
        self.shape = shape
        self.x = x
        self.y = y
        self.text = text
        self.command = command

    def draw(self, screen):
        DRAW_MAP[self.shape](
            screen, self.p_color, self.x, self.y, self.width, self.height
        )

    def in_button(self, x, y):
        return (
            x >= self.x
            and x <= self.x + self.width
            and y >= self.y
            and y <= self.y + self.height
        )

    def click(self, x, y):
        if self.in_button(x, y):
            self.command()
