import pygame

from Entities.Projectile import Projectile
from src.Assets import settings
from Entities.entity import Entity


class BigEnemy(Entity):
    def __init__(self, pos, *groups):
        self.init_images()
        super().__init__(self.char, 0, 0, pos)
        self.pos = pos
        self.animation_count = 0
        self.vel = pygame.Vector2((0, 0))
        self.speed = 4
        self.direction = settings.LEFT
        self.stats = {"health": 20000, "strength": 20}
        self.projectiles = []
        self.attack_counter = 0

    def init_images(self):
        self.char = pygame.image.load(settings.SPRITES_PATH + 'bos/idle_1.png')
        self.idle = [pygame.image.load(settings.SPRITES_PATH + 'bos/idle_1.png'),
                     pygame.image.load(settings.SPRITES_PATH + 'bos/idle_2.png'),
                     pygame.image.load(settings.SPRITES_PATH + 'bos/idle_3.png'),
                     pygame.image.load(settings.SPRITES_PATH + 'bos/idle_4.png'),
                     pygame.image.load(settings.SPRITES_PATH + 'bos/idle_5.png'),
                     pygame.image.load(settings.SPRITES_PATH + 'bos/idle_6.png'),
                     pygame.image.load(settings.SPRITES_PATH + 'bos/idle_7.png'),
                     pygame.image.load(settings.SPRITES_PATH + 'bos/idle_8.png'),
                     pygame.image.load(settings.SPRITES_PATH + 'bos/idle_9.png'),
                     pygame.image.load(settings.SPRITES_PATH + 'bos/idle_10.png')]

        self.idle = list(map(lambda x: pygame.transform.scale2x(x), self.idle))
        self.char = pygame.transform.scale2x(self.char)

        for ind, val in enumerate(self.idle):
            rect = val.get_rect()

        rect = self.char.get_rect()

    def anim(self):
        self.animation_count %= 50
        self.image = self.idle[self.animation_count // 5]
        self.animation_count += 1

    def update(self, player):
        self.attack_counter %= 60
        if self.attack_counter == 0:
            if len(self.projectiles) < 5:
                if self.direction == settings.LEFT:
                    self.projectiles.append(Projectile((round(self.rect.x) - 85, self.rect.top + 5), -1))
                else:
                    self.projectiles.append(Projectile((round(self.rect.x) + 15, self.rect.top + 5), 1))
        if player.rect.x > self.rect.x:
            self.direction = settings.RIGHT
            # self.vel.x = self.speed
        else:
            # self.vel.x = -self.speed
            self.direction = settings.LEFT

        if player.rect.y > self.rect.y:
            self.vel.y = self.speed
        else:
            self.vel.y = -self.speed
        self.attack_counter += 1
        self.anim()

    def is_alive(self):
        return self.stats["health"] > 0
