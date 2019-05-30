import pygame
from src.Entities.entity import Entity
from src.Assets import settings
from pygame import *
from src.Entities.platform import NextLevelPlatform, GameOverPlatform

class CollisionDetector():
    def __init__(self, platforms, entities, levelGenerator, *groups):
        self.platforms = platforms
        self.entities = entities
        self.levelGenerator = levelGenerator

    def update(self, player):
        player.rect.left += player.vel.x
        self.collide(player.vel.x, 0, player)
        player.rect.top += player.vel.y
        player.onGround = False
        self.collide(0, player.vel.y, player)

    def collide(self, xvel, yvel, player):
        for p in self.platforms:
            if pygame.sprite.collide_rect(player, p):
                if isinstance(p, NextLevelPlatform):
                    self.levelGenerator.load(2)
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
