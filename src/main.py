#!/usr/bin/env/python3
from src.Assets import settings
import pygame

pygame.init()
bg_image = pygame.image.load("Assets/PixelArt.png")
window_width = 800
window_height = 640
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Gameee")


class Player(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.heigth = height
        self.speed = 5
        self.jumping = False
        self.moving_right = False
        self.moving_left = False
        self.jump_count = 8
        self.walk_count = 0
        self.face = 1 # -1 for left, 1 for right
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

    def draw(self, game_window):

        self.walk_count = self.walk_count % 27

        if player.moving_left:
            game_window.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
            self.face = -1
        elif player.moving_right:
            game_window.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
            self.face = 1
        elif self.face == 1:
            game_window.blit(self.walk_right[0], (self.x, self.y))
        else:
            game_window.blit(self.walk_left[0], (self.x, self.y))

    def jump(self):

        if self.jump_count >= -8:
            direction = 1
            if self.jump_count < 0:
                direction = -1
            self.y -= (self.jump_count ** 2) * 0.5 * direction
            self.jump_count -= 1

        else:
            self.jumping = False
            self.jump_count = 8

    def shoot(self, game_window):
        pass

    def move(self):
        pass


bg = pygame.image.load(settings.SPRITES_PATH + 'bg.jpg')

clock = pygame.time.Clock()
running = True


def draw(player_obj):
    window.fill((0, 0, 0))
    window.blit(bg_image, (0, 0))
    player_obj.draw(window)
    pygame.display.update()


player = Player(40, 580, 64, 64)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if player.jumping:
        player.jump()
    else:
        if keys[pygame.K_UP]:
            player.jumping = True

        if keys[pygame.K_DOWN] and y < window_height - player.height - player.speed:
            player.y += player.speed

    # if keys[pygame.K_SPACE]:

    if keys[pygame.K_RIGHT] and player.x < window_width - player.width - player.speed:
        player.x += player.speed
        player.moving_right = True
        player.moving_left = False
    elif keys[pygame.K_LEFT] and player.x > player.speed:
        player.x -= player.speed
        player.moving_left = True
        player.moving_right = False
    else:
        player.moving_right = False
        player.moving_left = False
        player.walk_count = 0

    draw(player)
    clock.tick(60)
pygame.quit()
