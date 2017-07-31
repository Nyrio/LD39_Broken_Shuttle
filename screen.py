import pygame

class Screen:
    def __init__(self, caption = "", width = 800, height = 600,
                 framerate = 60):
        self.width = width
        self.height = height
        self.framerate = framerate

        self.canvas = pygame.display.set_mode([width, height])
        pygame.display.set_caption(caption)

        self.back = pygame.image.load("sprites/background.png").convert()