import pygame
from math import *


class Station:
    def __init__(self, x_expr, y_expr):
        self.x_expr = x_expr
        self.y_expr = y_expr
        self.sprite = pygame.image.load("sprites/station.png").convert_alpha()
        self.width, self.height = self.sprite.get_size()
        self.rx, self.ry = 30, 40

        self.update(0)


    def update(self, time):
        self.pos = (eval(self.x_expr.replace("t", str(time))),
                    eval(self.y_expr.replace("t", str(time))))


    def draw(self, canvas):
        x = self.pos[0] - self.width // 2
        y = self.pos[1] - self.height // 2
        canvas.blit(self.sprite, [x, y])