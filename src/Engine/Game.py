import pygame as pg
from src.Assets import settings
import pygame
from pygame import *
from src.Engine.Client import Client
from src.Entities.Enemy import Enemy

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
        self.client = Client(self.player, self.players, self.collisionDetector.enemies)
        self.client.run()

    def run(self):
        while self.player.is_alive():
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
            self.draw_enemies()
            self.draw_players()
            self.draw_hud()
            pygame.display.update()
            self.clock.tick(settings.FPS)
            #print(str(self.player.rect) + ' ' + str(self.player.vel))

        self.player.stats["health"] = 100
    def update_projectiles(self):
        for projectile in self.player.projectiles:
            if abs(projectile.x - self.player.win_x) > 800:
                self.player.projectiles.pop(self.player.projectiles.index(projectile))
            self.window.blit(projectile.image, (projectile.x, projectile.y))
            projectile.update()

    def draw_players(self):
        # print("PLAYERS:")
        for id, pos in self.players.items():
            # print(f"{id} : {pos}")
            if(self.client.id != id):
                self.window.blit(self.player.image, (pos[0] + self.entities.cam.x, pos[1]))

    def draw_enemies(self):
        for enemy in self.collisionDetector.enemies:
            enemy.update()
            self.window.blit(enemy.image, (enemy.rect.x + self.entities.cam.x, enemy.rect.y))
            pygame.draw.rect(self.window, (255, 0, 0), (enemy.rect.x + self.entities.cam.x, enemy.rect.y + 10,
                                                        enemy.stats["health"] // 4, 10))

    def draw_hud(self):
        pygame.draw.rect(self.window, (255, 0, 0), (30, 50, self.player.stats["health"] * 2, 18))

