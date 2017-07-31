import pygame

from level import Level

NB_LVLS = 7

class MainMenu():
    def __init__(self, screen):
        self.screen = screen
        self.framerate = screen.framerate
        self.clock = pygame.time.Clock()

        self.sprite = pygame.image.load("sprites/main_menu.png").convert()
        self.choose = pygame.image.load("sprites/choose_level.png").convert()

        self.lvl_font = pygame.font.Font("sprites/glacial_indiff.otf", 40)

    def start(self):
        while True:
            self.draw()
            self.clock.tick(self.framerate)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_ESCAPE)):
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x > 91 and x < 347 and y > 223 and y < 279:
                        if not self.play(self.read_save()):
                            return
                    elif x > 453 and x < 709 and y > 223 and y < 279:
                        if not self.choose_level():
                            return

    def draw(self):
        self.screen.canvas.blit(self.sprite, [0, 0])

        mx, my = pygame.mouse.get_pos()
        if mx > 91 and mx < 347 and my > 223 and my < 279:
            pygame.draw.rect(self.screen.canvas, [120, 120, 255],
                             [91, 223, 257, 56], 1)
        elif mx > 453 and mx < 709 and my > 223 and my < 279:
            pygame.draw.rect(self.screen.canvas, [120, 120, 255],
                             [453, 223, 257, 56], 1)
        pygame.display.flip()


    def play(self, lvl):
        res = 3
        while res != 1:
            if res == 3:
                level = Level(self.screen, "levels/level%d.txt" % lvl)
                if not level.intro():
                    return False
            else:
                level.init_shuttle()
                level.fade(0)
            res = level.start()
            if res == 3:
                lvl += 1
                if lvl == NB_LVLS+1:
                    self.congrats()
                    lvl = 1
                    res = 4
                self.write_save(lvl)
            if res == 4:
                return True
        return False


    def choose_level(self):
        while True:
            self.draw_choose()
            self.clock.tick(self.framerate)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_ESCAPE)):
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if mx > 50 and mx < 750 and my > 220 and my < 565:
                        ix = (mx - 50) // 124
                        iy = (my - 220) // 95
                        if (6*iy + ix < NB_LVLS and (mx - 50) % 124 < 80
                                                and (my - 220) % 95 < 60):
                            lvl = 6*iy + ix + 1

                            level = Level(self.screen,
                                          "levels/level%d.txt" % lvl)
                            if not level.intro():
                                return False
                            res = 0
                            while res == 0 or res == 2:
                                if res:
                                    level.init_shuttle()
                                    level.fade(0)
                                res = level.start()
                            if res == 1:
                                return False


    def draw_choose(self):
        self.screen.canvas.blit(self.choose, [0, 0])

        for i in range(NB_LVLS):
            ix = i % 6
            iy = i // 6
            pygame.draw.rect(self.screen.canvas, [200, 255, 255],
                             [50 + 124*ix, 220 + 95*iy, 80, 60], 1)
            text = self.lvl_font.render(str(i+1), True, [200, 255, 255])
            self.screen.canvas.blit(text, [90+124*ix - text.get_width() / 2,
                                           250+95*iy - text.get_height() / 2])

        mx, my = pygame.mouse.get_pos()
        if mx > 50 and mx < 750 and my > 220 and my < 565:
            ix = (mx - 50) // 124
            iy = (my - 220) // 95
            if (6*iy + ix < NB_LVLS and (mx - 50) % 124 < 80
                                    and (my - 220) % 95 < 60):
                pygame.draw.rect(self.screen.canvas, [120, 120, 255],
                                 [50 + 124*ix, 220 + 95*iy, 80, 60], 1)
        
        pygame.display.flip()


    def read_save(self):
        with open("levels/save.txt", 'r') as f:
            lvl = int(f.readlines()[0].replace('\n', ''))
        return lvl

    def write_save(self, lvl):
        with open("levels/save.txt", 'w') as f:
            f.write(str(lvl))


    def congrats(self):
        pass