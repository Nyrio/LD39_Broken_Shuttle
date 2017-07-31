import pygame
from math import *

from util import *

MOTOR_COEFF = 129.6
PLANET_COEFF = 1036800
G_EXP = 1.8
DEG_PER_SEC = 40

EXPL_RADIUS = 70


class Shuttle:
    def __init__(self, x, y, angle, energy):
        self.pos = (x, y)
        self.angle = angle
        self.energy = energy

        self.sprite = (
              pygame.image.load("sprites/shuttle_none.png").convert_alpha(),
              pygame.image.load("sprites/shuttle_left.png").convert_alpha(),
              pygame.image.load("sprites/shuttle_right.png").convert_alpha(),
              pygame.image.load("sprites/shuttle_both.png").convert_alpha(),
            )
        self.mv_type = 0

        self.broken = False
        self.broken_time = 0

        self.speed = (0, 0)
        self.acceleration = (0, 0)

        self.angle_speed = 0

        self.active = False
        self.last_thrust = 0
        self.angle_speed_last_thrust = 0


    def update(self, dtime, left, right, planets):
        # User input
        self.mv_type = 0
        if self.energy > 0:
            self.mv_type = left + 2*right
            if self.mv_type == 1:
                self.angle_speed = - DEG_PER_SEC
            elif self.mv_type == 2:
                self.angle_speed = DEG_PER_SEC
            elif self.mv_type == 3:
                self.angle_speed = 0
            power = left + right
            if self.mv_type:
                self.active = True
                self.last_thrust = 0
                self.angle_speed_last_thrust = self.angle_speed
            self.energy -= power * dtime
            if self.energy < 0: self.energy = 0
        else:
            power = 0

        if not self.mv_type:
            self.last_thrust += dtime
            if self.last_thrust > 3:
                self.angle_speed = 0
            else:
                self.angle_speed = (self.angle_speed_last_thrust
                                    * (1 - self.last_thrust / 3))

        self.angle += self.angle_speed * dtime

        thrust = (MOTOR_COEFF * power * cos(radians(self.angle)),
                 -MOTOR_COEFF * power * sin(radians(self.angle)))

        # Interaction with planets
        gravity = (0, 0)
        if self.active:
            for planet in planets:
                to_planet = (planet.pos[0]-self.pos[0], planet.pos[1]-self.pos[1])
                d = norm(to_planet)
                unit = t_prod(1/d, to_planet)
                ampl = PLANET_COEFF * planet.mass / (d**G_EXP)

                gravity = t_sum(gravity, t_prod(ampl, unit))

        # Physics
        self.acceleration = t_sum(thrust, gravity)
        self.speed = t_sum(self.speed, t_prod(dtime, self.acceleration))

        self.pos = t_sum(self.pos, t_prod(dtime, self.speed))


    def draw(self, canvas):
        if self.broken:
            pygame.draw.circle(canvas, [255,255,180],
                (int(self.pos[0]),int(self.pos[1])),
                 int(EXPL_RADIUS*interp(self.broken_time)))
            return

        sprite = self.sprite[self.mv_type]
        rotated = pygame.transform.rotozoom(sprite, self.angle, 1)
        width, height = rotated.get_size()
        x = self.pos[0] - width // 2
        y = self.pos[1] - height // 2
        canvas.blit(rotated, [x, y])

        # for v in self.vertices():
        #     pygame.draw.rect(canvas,[0,255,0],[v[0]-1,v[1]-1,2,2],1)


    def vertices(self):
        vert_model = [(-10,-12), (1, -7), (20, -6), (26, 0), (20, 6),
                      (1, 7), (-10, 12)]
        c = cos(radians(self.angle))
        s = sin(radians(-self.angle))
        return [t_sum(self.pos, (v[0]*c - v[1]*s, v[0]*s + v[1]*c))
                    for v in vert_model]

def interp(t):
    return 1 - exp(-t / 0.1)