import pygame
from math import *


class Planet:
    def __init__(self, x_expr, y_expr, angle_expr, radius, mass, filename):
        self.x_expr = x_expr
        self.y_expr = y_expr
        self.angle_expr = angle_expr
        self.radius = radius
        self.mass = mass
        self.sprite = pygame.image.load(filename).convert_alpha()

        self.update(0)


    def update(self, time):
        self.pos = (eval(self.x_expr.replace("t", str(time))),
                    eval(self.y_expr.replace("t", str(time))))
        self.angle = eval(self.angle_expr.replace("t", str(time)))


    def draw(self, canvas):
        rotated = pygame.transform.rotozoom(self.sprite, self.angle, 1)
        width, height = rotated.get_size()
        x = self.pos[0] - width // 2
        y = self.pos[1] - height // 2
        canvas.blit(rotated, [x, y])

        # pygame.draw.rect(canvas,[0,255,0],
        #                  [self.pos[0]-self.radius,self.pos[1]-self.radius,
        #                   2*self.radius, 2*self.radius],1)