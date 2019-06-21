import pygame
from src.Entities.entity import Entity
from src.Assets import settings
from pygame import *
from src.Entities.platform import NextLevelPlatform, GameOverPlatform


class CollisionDetector:
    def __init__(self, platforms, entities, levelGenerator, enemies, *groups):
        self.platforms = platforms
        self.entities = entities
        self.levelGenerator = levelGenerator
        self.players = []
        self.enemies = enemies

    def add_player(self, player):
        self.players.append(player)

    def del_player(self, player):
        self.players.remove(player)

    def update(self):
        for enemy in self.enemies:
            enemy.rect.left += enemy.vel.x
            self.collide_enemy(enemy.vel.x, 0, enemy)
            enemy.rect.top += enemy.vel.y
            enemy.onGround = False
            self.collide_enemy(0, enemy.vel.y, enemy)
        for player in self.players:
            player.rect.left += player.vel.x
            self.collide(player.vel.x, 0, player)
            player.rect.top += player.vel.y
            player.onGround = False
            self.collide(0, player.vel.y, player)
            for projectile in player.projectiles:
                projectile.rect.left += projectile.vel.x
            self.dmg_collider(self.enemies[0], player)
            self.dmg_collider(self.enemies[1], player)


    def collide(self, xvel, yvel, player):
        for p in self.platforms:
            if pygame.sprite.collide_rect(player, p):
                if isinstance(p, NextLevelPlatform):
                    self.levelGenerator.load(2)
                    for player in self.players:
                        player.rect = player.image.get_rect(topleft=settings.STARTING_POS)
                if isinstance(p, GameOverPlatform):
                    exit()                                  #TODO: main menu instead (?)
                if xvel > 0:
                    player.rect.right = p.rect.left
                if xvel < 0:
                    player.rect.left = p.rect.right
                if yvel > 0:
                    player.rect.bottom = p.rect.top
                    player.onGround = True
                    player.vel.y = 0
                if yvel < 0:
                    player.rect.top = p.rect.bottom

    def collide_enemy(self, xvel, yvel, enemy):
        for p in self.platforms:
            if pygame.sprite.collide_rect(enemy, p):
                if xvel > 0:
                    enemy.rect.right = p.rect.left
                if xvel < 0:
                    enemy.rect.left = p.rect.right
                if yvel > 0:
                    enemy.rect.bottom = p.rect.top
                    enemy.onGround = True
                    enemy.vel.y = 0
                if yvel < 0:
                    enemy.rect.top = p.rect.bottom

    def dmg_collider(self, enemy, player):
        if pygame.sprite.collide_rect(enemy, player) and enemy.is_alive():
            player.stats["health"] -= 0.9
        for projectile in player.projectiles:
            print(projectile.rect.x, enemy.rect.x)
            if pygame.sprite.collide_rect(projectile, enemy):
                enemy.stats["health"] -= 30
    # def collide_projectile(self,enemy,player):
    #     for projectile in player.projectiles:
