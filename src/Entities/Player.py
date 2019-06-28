import pygame
from src.Entities.entity import Entity
from src.Assets import settings
from pygame import *
from src.Entities.Projectile import Projectile
from src.Entities.platform import NextLevelPlatform


class Player(Entity):
    def __init__(self, pos, *groups):
        self.stats = {"health": settings.PLAYER_HEALTH}
        self.init_images()
        super().__init__(self.char, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT, pos)
        self.vel = pygame.Vector2((0, 0))
        self.onGround = False
        self.jump_strength = settings.PLAYER_JUMP_STRENGTH
        self.speed = settings.PLAYER_SPEED
        self.walk_count = 0
        self.direction = "facing_right"
        self.projectiles = []
        # self.char = pygame.image.load(settings.SPRITES_PATH + 'standing.png')

    def reset(self):
        self.rect.x = settings.STARTING_POS[0]
        self.rect.y = settings.STARTING_POS[1]
        self.stats["health"] = settings.PLAYER_HEALTH
        self.vel = pygame.Vector2((0, 0))
        self.onGround = False
        self.walk_count = 0
        self.direction = "facing_right"
        self.projectiles = []

    def init_images(self):
        self.char = pygame.image.load(settings.SPRITES_PATH + 'char2/right_1.png')
        self.char_left = pygame.image.load(settings.SPRITES_PATH + 'char2/left_1.png')
        self.char_right = pygame.image.load(settings.SPRITES_PATH + 'char2/right_1.png')
        self.walk_right = [pygame.image.load(settings.SPRITES_PATH + 'char2/right_1.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'char2/right_2.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'char2/right_3.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'char2/right_4.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'char2/right_5.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'char2/right_6.png'),
                           # pygame.image.load(settings.SPRITES_PATH + 'R7.png'),
                           # pygame.image.load(settings.SPRITES_PATH + 'R8.png'),
                           # pygame.image.load(settings.SPRITES_PATH + 'R9.png')]
        ]
        self.walk_left = [pygame.image.load(settings.SPRITES_PATH + 'char2/left_1.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'char2/left_2.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'char2/left_3.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'char2/left_4.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'char2/left_5.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'char2/left_6.png'),
                          # pygame.image.load(settings.SPRITES_PATH + 'L7.png'),
                          # pygame.image.load(settings.SPRITES_PATH + 'L8.png'),
                          # pygame.image.load(settings.SPRITES_PATH + 'L9.png')]
        ]

        for ind, val in enumerate(self.walk_right):
            rect = val.get_rect()

        for ind, val in enumerate(self.walk_left):
            rect = val.get_rect()

        rect = self.char.get_rect()

    def anim(self, direction):
        self.walk_count = self.walk_count % 18
        if direction == "left":
            self.image = self.walk_left[self.walk_count // 3]
            self.walk_count += 1
        elif direction == "right":
            self.image = self.walk_right[self.walk_count // 3]
            self.walk_count += 1
        elif direction == "facing_left":
            self.image = self.char_left
        elif direction == "facing_right":
            self.image = self.char_right

    def update(self, mv=None):
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        space = pressed[K_SPACE]
        attack = pressed[K_q]
        heal = pressed[K_h]

        # normal keyboard input
        if heal:
            self.stats["health"] += 20
        if attack:
            if len(self.projectiles) < 1:
                if self.direction == "facing_left":
                    self.projectiles.append(Projectile((round(self.rect.x) - 85, self.rect.top + 5), -1))
                else:
                    self.projectiles.append(Projectile((round(self.rect.x) + 15, self.rect.top + 5), 1))
        if space or up:
            if self.onGround:
                self.vel.y = -self.jump_strength
        if left:
            self.vel.x = -self.speed
            self.anim("left")
            last = "last_left"
            self.direction = "facing_left"
        if right:
            self.vel.x = self.speed
            self.anim("right")
            self.direction = "facing_right"
        if not self.onGround:
            self.vel.y += settings.PLAYER_GRAVITY
            if self.vel.y > settings.MAX_FALLING_SPEED: self.vel.y = settings.MAX_FALLING_SPEED
            # print('Predkosc vel.y: ' + str(self.vel.y))
        if not (left or right):
            self.vel.x = 0
            self.anim(self.direction)

    def update_relative_position(self, x):
        self.win_x = x

    def is_alive(self):
        return self.stats["health"] > 0
