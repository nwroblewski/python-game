import pygame
from src.Assets import settings
from src.Entities.platform import *


class LevelGenerator:
    def __init__(self, platforms, entities):
        self.platforms = platforms
        self.entities = entities
        self.tiles = [pygame.image.load(settings.SPRITES_PATH + 'tile1.png'),
                pygame.image.load(settings.SPRITES_PATH + 'tile2.png'),
                pygame.image.load(settings.SPRITES_PATH + 'tileN.png'),
                pygame.image.load(settings.SPRITES_PATH + 'tileG.png')]

        for ind, val in enumerate(self.tiles):
            rect = val.get_rect()
            if not (rect.width == settings.TILE_SIZE and rect.height == settings.TILE_SIZE):
                self.tiles[ind] = pygame.transform.scale(self.tiles[ind], (settings.TILE_SIZE, settings.TILE_SIZE))

    def load(self, level):
        for p in self.platforms:
            p.kill()
        
        f = open(settings.LEVELS_PATH + str(level), "r")
        x = 0
        y = 0
        for line in f.readlines():
            for char in line:
                if char == "1":
                    Platform(self.tiles[0], (x, y), self.platforms, self.entities)
                elif char == "2":
                    Platform(self.tiles[1], (x, y), self.platforms, self.entities)
                elif char == "N":
                    NextLevelPlatform(self.tiles[2], (x, y), self.platforms, self.entities)
                elif char == "G":
                    GameOverPlatform(self.tiles[3], (x, y), self.platforms, self.entities)
                x += settings.TILE_SIZE
            x = 0
            y += settings.TILE_SIZE
        f.close()
