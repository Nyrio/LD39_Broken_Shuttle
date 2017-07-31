##############################################################################
#                                                                            #
#  A game by Louis Sugy for Ludum Dare #39                                   #
#  Theme: Running out of power                                               #
#                                                                            #
#  CC BY-NC-SA                                                               #
#                                                                            #
##############################################################################

import pygame

from screen import Screen
from menu import MainMenu
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = Screen("Broken Shuttle by Louis Sugy", 800, 600, 60)
        self.clock = pygame.time.Clock()

    def start(self):
        main_menu = MainMenu(self.screen)
        main_menu.start()

    def end(self):
        pygame.quit()


game = Game()
try:
    game.start()
finally:
    game.end()