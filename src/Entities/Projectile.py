import pygame
from src.Assets import settings
from src.Entities.entity import Entity


class Projectile(Entity):

    def __init__(self, pos, direction, *groups):
        self.direction = direction
        self.init_images()
        super().__init__(self.sprite, 0, 0, pos)
        self.vel = pygame.Vector2((0, 0))
        self.speed = 7
        self.direction = direction

    def init_images(self):
        if self.direction == -1:
            self.sprite = pygame.image.load(settings.SPRITES_PATH + 'projectile_left.png')
        else:
            self.sprite = pygame.image.load(settings.SPRITES_PATH + 'projectile_right.png')

        rect = self.sprite.get_rect()

    def __getstate__(self):
        pickleable_dict = dict((k, v) for k, v in self.__dict__.items() if k in ['direction', 'rect'])
        return pickleable_dict

    def update(self):
        self.vel.x = self.speed * self.direction
