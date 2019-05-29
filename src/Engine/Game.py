import pygame as pg
from src.Assets import settings
import pygame
from pygame import *


class Game:
    def __init__(self, player, entities):
        self.clock = pygame.time.Clock()
        self.player = player
        self.entities = entities

    def new_game(self):
        pass

    def run(self, window):
        while 1:
            for e in pygame.event.get():
                if e.type == QUIT:
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    return

            self.entities.update()

            window.fill((0, 0, 0))
            self.entities.draw(window)
            pygame.display.update()
            self.clock.tick(settings.FPS)










