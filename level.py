import pygame

from shuttle import Shuttle
from planet import Planet
from station import Station

from util import *

class Level:
    def __init__(self, screen, filename):

        # Read level file
        with open(filename, 'r') as f:
            lines = list(map(lambda x: x.replace('\n',''), f.readlines()))
        i = lines.index("#player") + 1
        p = map(float, lines[i].split(" "))
        self.shuttle_orig = tuple(p)
        self.init_shuttle()

        self.planets = []

        i = lines.index("#planets") + 1
        while lines[i]:
            p = lines[i].split(" ")
            self.planets.append(Planet(*p[:3], int(p[3]), float(p[4]), p[5]))
            i += 1

        i = lines.index("#station") + 1
        self.station = Station(*lines[i].split(" "))

        self.dialog = []
        i = lines.index("#intro") + 1
        while i < len(lines) and lines[i]:
            self.dialog.append((int(lines[i][0]), lines[i][2:]))
            i += 1

        i = lines.index("#end") + 1
        self.end = (int(lines[i][0]), lines[i][2:])

        # Take game info
        self.screen = screen
        self.canvas = screen.canvas
        self.framerate = screen.framerate
        self.clock = pygame.time.Clock()

        self.time = 0

        # Load sprites
        self.chara1 = pygame.image.load("sprites/pilot.png").convert_alpha()
        self.chara2 = pygame.image.load("sprites/copilot.png").convert_alpha()

        self.power = pygame.image.load("sprites/energy.png").convert_alpha()

        # Load fonts
        self.dialog_font = pygame.font.Font("sprites/glacial_indiff.otf", 22)


    def init_shuttle(self):
        self.shuttle = Shuttle(*self.shuttle_orig)


    def intro(self):
        self.fade(0)
        pygame.event.clear()
        for (character, text) in self.dialog:
            res = self.message(character, text)
            if not res:
                return False
            elif res == 1:
                break
        return True


    def start(self):
        pygame.event.clear()
        while True:
            res = self.update()
            if res:
                return res
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.framerate)


    def update(self):
        # Return values:
        # 0: no special event
        # 1: player quits
        # 2: player fails or restart
        # 3: player win
        # 4: player goes back to menu

        vertices = self.shuttle.vertices()

        # Check if player is out of screen
        out = 0
        for v in vertices:
            if (v[0] < -20 or v[0] > self.screen.width+20
             or v[1] < -20 or v[1] > self.screen.height+20):
                out += 1
        if out == len(vertices):
            self.lost()
            return 2

        # Collision detection
        for planet in self.planets:
            for v in vertices:
                if (norm((v[0]-planet.pos[0], v[1]-planet.pos[1]))
                  < planet.radius):
                    collide = True
                    self.collision()
                    return 2

        # Arrival detection
        for v in vertices:
            if (v[0] >= self.station.pos[0] - self.station.rx
              and v[0] <= self.station.pos[0] + self.station.rx
              and v[1] >= self.station.pos[1] - self.station.ry
              and v[1] <= self.station.pos[1] + self.station.ry):
                self.arrival()
                return 3



        dtime = 1 / self.framerate
        self.time += dtime

        left, _, right = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.fade(1)
                    return 2
                if event.key == pygame.K_ESCAPE:
                    return 4

        self.shuttle.update(dtime, left, right, self.planets)

        self.station.update(self.time)

        for planet in self.planets:
            planet.update(self.time)

        return 0


    def draw(self):
        self.canvas.blit(self.screen.back, [0,0])

        for planet in self.planets:
            planet.draw(self.canvas)

        self.station.draw(self.canvas)
        self.shuttle.draw(self.canvas)

        if self.shuttle.energy > 0:
            rect_black = pygame.Rect([30, 6, 100*self.shuttle.energy+2, 29])
            rect_yellow = pygame.Rect([30, 8, 100*self.shuttle.energy, 25])

            pygame.draw.rect(self.canvas, [0,0,0], rect_black)
            self.canvas.fill([255,255,0], rect_yellow)

        self.canvas.blit(self.power, [2,2])


    def message(self, character, text):
        txt_width = self.dialog_font.render(text, True,
                                            [255, 255, 255]).get_width()

        i = 0
        next = False
        while not next:
            self.station.update(self.time)

            for planet in self.planets:
                planet.update(self.time)

            self.draw()

            text_disp = self.dialog_font.render(text[:i+1],
                                                True, [255, 255, 255])

            if character == 0:
                self.canvas.blit(self.chara1, [0, 339])
                self.canvas.blit(text_disp, [230, 550])
            else:
                self.canvas.blit(self.chara2, [539, 339])
                self.canvas.blit(text_disp, [519 - txt_width, 550])

            pygame.display.flip()
            self.clock.tick(self.framerate)
            self.time += 1 / self.framerate

            if i == len(text) - 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 0
                    if (event.type == pygame.KEYDOWN
                        and (event.key == pygame.K_SPACE
                             or event.key == pygame.K_RETURN)):
                        return 1
                    if event.type == pygame.MOUSEBUTTONUP:
                        next = True
            else:
                i += 1

        return 2


    def lost(self):
        self.fade(1)

    def collision(self):
        self.shuttle.broken = True
        self.fade(1)

    def arrival(self):
        self.message(self.end[0], self.end[1])
        self.fade(1)


    def fade(self, mode):
        black_rect = pygame.Surface((800, 600))
        black_rect.fill([0, 0, 0])
        for i in range(self.framerate // 2):
            self.station.update(self.time)

            for planet in self.planets:
                planet.update(self.time)

            if self.shuttle.broken:
                self.shuttle.broken_time += 1 / self.framerate

            self.draw()

            alpha = 510 * i / self.framerate
            if not mode: alpha = 255 - alpha
            black_rect.set_alpha(alpha)
            self.canvas.blit(black_rect, [0, 0])

            pygame.display.flip()

            self.clock.tick(self.framerate)
            self.time += 1 / self.framerate