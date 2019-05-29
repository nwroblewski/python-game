import pygame
from src.Entities.entity import Entity
from src.Assets import settings
from pygame import *


class Player(Entity):
    def __init__(self, platforms, pos, *groups):
        self.init_images()
        super().__init__(self.char, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT, pos)
        self.vel = pygame.Vector2((0, 0))
        self.onGround = False
        self.jump_strength = settings.PLAYER_JUMP_STRENGTH
        self.platforms = platforms
        self.speed = settings.PLAYER_SPEED
        self.walk_count = 0

        # self.char = pygame.image.load(settings.SPRITES_PATH + 'standing.png')

    def init_images(self):
        self.char = pygame.image.load(settings.SPRITES_PATH + 'standing.png')
        self.walk_right = [pygame.image.load(settings.SPRITES_PATH + 'R1.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'R2.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'R3.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'R4.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'R5.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'R6.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'R7.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'R8.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'R9.png')]
        self.walk_left = [pygame.image.load(settings.SPRITES_PATH + 'L1.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'L2.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'L3.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'L4.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'L5.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'L6.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'L7.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'L8.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'L9.png')]

        for ind, val in enumerate(self.walk_right):
            rect = val.get_rect()
            if not (rect.width == settings.PLAYER_WIDTH and rect.height == settings.PLAYER_HEIGHT):
                self.walk_right[ind] = pygame.transform.scale(self.walk_right[ind],
                                                              (settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT))

        for ind, val in enumerate(self.walk_left):
            rect = val.get_rect()
            if not (rect.width == settings.PLAYER_WIDTH and rect.height == settings.PLAYER_HEIGHT):
                self.walk_left[ind] = pygame.transform.scale(self.walk_left[ind],
                                                             (settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT))

        rect = self.char.get_rect()
        if not (rect.width == settings.PLAYER_WIDTH and rect.height == settings.PLAYER_HEIGHT):
            self.char = pygame.transform.scale(self.char, (settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT))

    def anim(self, direction):
        self.walk_count = self.walk_count % 27
        if direction == "left":
            self.image = self.walk_left[self.walk_count // 3]
            self.walk_count += 1
        elif direction == "right":
            self.image = self.walk_right[self.walk_count // 3]
            self.walk_count += 1
        elif direction == "stand":
            self.image = self.char

    def update(self):
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        space = pressed[K_SPACE]

        if space or up:
            if self.onGround:
                self.vel.y = -self.jump_strength
        if left:
            self.vel.x = -self.speed
            self.anim("left")
        if right:
            self.vel.x = self.speed
            self.anim("right")
        if not self.onGround:
            self.vel.y += settings.PLAYER_GRAVITY
            if self.vel.y > settings.MAX_FALLING_SPEED: self.vel.y = settings.MAX_FALLING_SPEED
            # print('Predkosc vel.y: ' + str(self.vel.y))
        if not (left or right):
            self.vel.x = 0
            self.anim("stand")
        self.rect.left += self.vel.x
        self.collide(self.vel.x, 0, self.platforms)
        self.rect.top += self.vel.y
        self.onGround = False
        self.collide(0, self.vel.y, self.platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                # if isinstance(p, ExitBlock):                       # CHECKPOINT?
                #    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
