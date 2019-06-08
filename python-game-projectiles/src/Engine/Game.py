import pygame as pg
from src.Assets import settings
import pygame
from pygame import *


class Game:
    def __init__(self, entities, collisionDetector, bg):
        self.clock = pygame.time.Clock()
        self.players = []
        self.entities = entities
        self.bg = bg
        self.collisionDetector = collisionDetector

    def new_game(self):
        pass

    def add_player(self, player):
        self.players.append(player)
        player.rect = player.image.get_rect(topleft=settings.STARTING_POS)

    def run(self, window):
        while 1:
            for e in pygame.event.get():
                if e.type == QUIT:
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    return
            self.entities.update()
            for player in self.players:
                player.update_relative_position(player.rect.right + self.entities.cam.x)
            self.collisionDetector.update()
            window.blit(self.bg, (0, 0))
            self.update_projectiles(window)
            self.entities.draw(window)
            pygame.display.update()
            self.clock.tick(settings.FPS)
            #print(str(self.player.rect) + ' ' + str(self.player.vel))

    def update_projectiles(self, window):
        for player in self.players:
            for projectile in player.projectiles:
                if abs(projectile.x - player.win_x) > 800:
                    player.projectiles.pop(player.projectiles.index(projectile))
                projectile.draw(window)
                projectile.update()
