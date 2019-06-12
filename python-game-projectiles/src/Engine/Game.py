import pygame as pg
from src.Assets import settings
import pygame
from pygame import *
from src.Engine.Client import Client


class Game:
    def __init__(self, player, entities, collisionDetector, bg, window):
        self.clock = pygame.time.Clock()
        self.player = player
        self.players = {}
        self.entities = entities
        self.bg = bg
        self.collisionDetector = collisionDetector
        self.window = window

    def start_communication(self):
        self.client = Client(self.player, self.players)
        self.client.run()

    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.client.tcp_sock.send(b'd|')
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    self.client.tcp_sock.send(b'd|')
                    return
            self.entities.update()
            self.player.update_relative_position(self.player.rect.right + self.entities.cam.x)
            self.collisionDetector.update()
            self.window.blit(self.bg, (0, 0))
            self.update_projectiles()
            self.entities.draw(self.window)
            self.draw_players()
            pygame.display.update()
            self.clock.tick(settings.FPS)
            #print(str(self.player.rect) + ' ' + str(self.player.vel))

    def update_projectiles(self):
        for projectile in self.player.projectiles:
            if abs(projectile.x - self.player.win_x) > 800:
                self.player.projectiles.pop(self.player.projectiles.index(projectile))
            projectile.draw(self.window)
            projectile.update()

    def draw_players(self):
        print("PLAYERS:")
        for id, pos in self.players.items():
            print(f"{id} : {pos}")
            if(self.client.id != id):
                self.window.blit(self.player.image, pos)
