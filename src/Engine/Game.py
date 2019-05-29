import pygame as pg
from src.Assets import settings
import pygame
from pygame import *


class Game:
    def __init__(self, player, entities, bg):
        self.clock = pygame.time.Clock()
        self.player = player
        self.entities = entities
        self.bg = bg

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
            self.player.update_relative_position(self.player.rect.right + self.entities.cam.x)
            window.blit(self.bg, (0, 0))
            self.update_projectiles(window)
            self.entities.draw(window)
            pygame.display.update()
            self.clock.tick(settings.FPS)

    def update_projectiles(self, window):
        for projectile in self.player.projectiles:
            if abs(projectile.x - self.player.win_x) > 800:
                self.player.projectiles.pop(self.player.projectiles.index(projectile))
            projectile.draw(window)
            projectile.update()








