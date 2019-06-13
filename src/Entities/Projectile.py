import pygame
from src.Assets import settings

class Projectile:

    # TODO add fancy projectile animation here
    def __init__(self, x, y, radius, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.direction = direction
        self.velocity = 7 * direction
        self.init_images()

    def init_images(self):
        if self.direction == -1:
            self.image = pygame.image.load(settings.SPRITES_PATH + 'projectile_left.png')
        else:
            self.image = pygame.image.load(settings.SPRITES_PATH + 'projectile_right.png')

        self.rect = self.image.get_rect()

    def update(self):
        self.x += self.velocity
