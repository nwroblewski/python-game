import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, width, height, pos, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
