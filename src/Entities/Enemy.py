from src.Entities.entity import Entity
import pygame
from src.Assets import settings


class Enemy(Entity):
    def __init__(self, pos, *groups):
        self.init_images()
        super().__init__(self.char, 0, 0, pos)
        self.pos = pos
        self.walk_count = 0
        self.vel = pygame.Vector2((0, 0))
        self.speed = 2
        self.direction = settings.LEFT
        self.stats = {"health": 200, "strength": 20}
        self.is_attacking = False
        self.facing = settings.LEFT
        self.on_ground = False

    def init_images(self):
        self.char = pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_1.png')
        self.char_left = pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_1.png')
        self.char_right = pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_1.png')

        self.walk_left = [pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_1.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_2.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_3.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_4.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_5.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_6.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_7.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_8.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_9.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_10.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_11.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_12.png'),
                          pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_left_13.png')]

        self.walk_right = [pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_1.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_2.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_3.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_4.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_5.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_6.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_7.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_8.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_9.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_10.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_11.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_12.png'),
                           pygame.image.load(settings.SPRITES_PATH + 'skeleton_game/s_right_13.png')]

        self.walk_right = list(map(lambda x: pygame.transform.scale2x(x), self.walk_right))
        self.walk_left = list(map(lambda x: pygame.transform.scale2x(x), self.walk_left))

        self.char = pygame.transform.scale2x(self.char)
        self.char_left = pygame.transform.scale2x(self.char_left)
        self.char_right = pygame.transform.scale2x(self.char_right)

        for ind, val in enumerate(self.walk_right):
            rect = val.get_rect()

        for ind, val in enumerate(self.walk_left):
            rect = val.get_rect()

        rect = self.char.get_rect()

    def anim(self):
        self.walk_count %= 36
        if self.direction == settings.LEFT:
            self.image = self.walk_left[self.walk_count // 3]
            self.walk_count += 1
        elif self.direction == settings.RIGHT:
            self.image = self.walk_right[self.walk_count // 3]
            self.walk_count += 1
        # elif self.facing == settings.LEFT:
        #     self.image = self.char_left
        # elif self.facing == settings.RIGHT:
        #     self.image = self.char_right

    # TODO movement here
    def update(self):
        self.vel.x = -self.speed
        self.direction = settings.LEFT
        self.anim()

        if not self.on_ground:
            self.vel.y += settings.PLAYER_GRAVITY
            if self.vel.y > settings.MAX_FALLING_SPEED: self.vel.y = settings.MAX_FALLING_SPEED
            y = self.pos[1]
            y += self.vel.y
            self.pos = (50, y)
